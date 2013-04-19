#/bin/bash

python=`which python`
mysql=`which mysql`
sed=`which sed`
project_dir="../mangezmieux"
admin_script="${project_dir}/manage.py syncdb --noinput"
auth_models="${project_dir}/auth/models.py"
pattern_a_commenter="\tpost_save\."

#valeurs par défaut pour la connexion a la db
db_host="localhost"
db_user="root"
db_password="root"
db_name="mangez_mieux"

# Affichage de l'aide simplifiée
print_usage() {
	echo "Usage $0 [-h] [-H <db_hostname>] [-u <db_user> -p <db_password> -d <db_name>]\n"	
}

# Affichage de l'aide
print_help() {
	echo "Script d'installation de la base de données et des données initiales de MangezMieux\n\n"
	print_usage
	cat << EOF
-h
	print this help message
-H <db_host>
	specify the MangezMieux DB host
-d <db_name>
	specify the MangezMieux DB name
-u <db_user>
	specify the MangezMieux DB user
-p <db_password>
	specify the MangezMieux DB password
EOF
}


# Installation de la base de données
install_db() {
	${sed} -i "s/${pattern_a_commenter}/\#${pattern_a_commenter}/g" ${auth_models}
	echo "Recréation de la base de données\n"
	${mysql} -h ${db_host} -u ${db_user} -p${db_password} -e "DROP DATABASE IF EXISTS ${db_name}; CREATE DATABASE ${db_name};"
	echo "Insertion des données\n"
	${python} ${admin_script}
	echo "Création des index fulltext\n"
	${mysql} -h ${db_host} -u ${db_user} -p${db_password} ${db_name} -e "CREATE FULLTEXT INDEX recette_tags on core_recette (tags);"
	${sed} -i "s/\#${pattern_a_commenter}/${pattern_a_commenter}/g" ${auth_models}
}


while getopts "hH:u:p:d:" opt; 
do
	case ${opt} in
		h)
			print_help
			exit 1
			;;
		H)
			db_host=$OPTARG
			;;
		u)
			db_user=$OPTARG
			;;
		p)
			db_password=$OPTARG
			;;
		d)
			db_name=$OPTARG
			;;
		\? ) 
			echo "UNKNOWN wrong parameter\n"
			exit 1
			;;
	esac
done

install_db
exit 0

