#!/usr/bin/env perl

########################################################
# Version : 1.0
# Date : Apr 03 2013
# Author : maxibgoode
########################################################

use strict;
use warnings;
use Getopt::Long;
use LWP::Simple;
use JSON qw( decode_json );
use DBI;

# Openfoodfacts.org API URL : complete with <productid>.json
use constant URL => "http://fr.openfoodfacts.org/api/v0/product/";

# Opts
my $o_help = undef;
my $o_source = undef;
my $o_host = "localhost";
my $o_db = undef;
my $o_user = undef;
my $o_passwd = undef;
my @products = ();

# Routine to print script usage
sub print_usage {
	print "Usage: $0 [-h|--help] -s|--source <data.csv> [-H|--host <db_hostname>] -d|--db <db_name> -u|--user <db_user> -p|--password <db_password>\n";
}

# Routine to show help
sub help {
	print "\nScript d'export des produits d'openfoodfacts.org vers la base de données MangezMieux à partir d'un fichier CSV généré par le site : http://fr.openfoodfacts.org/cgi/search.pl\n\n";
	print_usage();
	print <<EOT;
-h, --help
	print this help message
-s, --source <data.csv>
	use <data.csv> as data source
-H, --host <db_host>
	specify the MangezMieux DB host
-d, --db <db_name>
	specify the MangezMieux DB name
-u, --user <db_user>
	specify the MangezMieux DB user
-p, --password <db_password>
	specify the MangezMieux DB password
EOT
}

# Routine to check script parameters
sub check_options {
	Getopt::Long::Configure('bundling');
	GetOptions(
	'h|help'	=> \$o_help,
	's|source=s' => \$o_source,
	'H|host:s' => \$o_host,
	'd|db=s' => \$o_db,
	'u|user=s' => \$o_user,
	'p|password=s' => \$o_passwd
	);
}

# Routine to get the json of a product by it's id
sub get_product_by_id {
	my ($id) = @_;
	my $product = get(URL.$id.".json");
	push(@products, $product);
}

# Routine to read the CSV, get the 1st field (product_id)
# and get 
sub get_products {
	my $file = $o_source;
	if( -f $file && -r $file ) {
		open (my $data, '<', $file) or die "Could not open $file\n";
###
###	TODO: Supprimer limitation aux 10 premiers produits
###
		my $i = 0;
		while (my $line = <$data> and $i++ < 10) {
			chomp $line;
			my @fields = split "\t" , $line;
			my $id = $fields[0];
			get_product_by_id($id);
		}
	}
}

# Routine to import the json into the MangezMieux DB
sub import {
	my $product;
	# DB connection
	my $db_co = DBI->connect(
		"DBI:mysql:database=$o_db;host=$o_host",
		$o_user, 
		$o_passwd
	)
	or die "Cannot connect to MySQL\n";	
	# Insert data for each product
	foreach $product (@products) {
		my $json = decode_json($product);
		if ( $json->{'status'} == 1 
			and defined($json->{'product'}{'nutriments'}) ) {
			# Insert nutriments
			my $energie = $json->{'product'}{'nutriments'}{'energy'};
			my $proteines = $json->{'product'}{'nutriments'}{'proteins'};
			my $glucides = $json->{'product'}{'nutriments'}{'sugars'};
			my $lipides = $json->{'product'}{'nutriments'}{'fat'};
			my $fibres = $json->{'product'}{'nutriments'}{'fiber'};
			my $sodium = $json->{'product'}{'nutriments'}{'sodium'};
			my $query = "INSERT INTO core_valeurnutritionnelle(";
			my $values;
			if (defined($energie)){$query .= "energie"; $values="VALUES($energie"}
			else {next;}
			if (defined($proteines)){$query .= ",proteines"; $values .= ",$proteines"}
			if (defined($glucides)){$query .= ",glucides"; $values .= ",$glucides"}
			if (defined($lipides)){$query .= ",lipides"; $values .= ",$lipides"}
			if (defined($fibres)){$query .= ",fibres"; $values .= ",$fibres"}
			if (defined($sodium)){$query .= ",sodium"; $values .= ",$sodium"}
			$query .= ")"; $values .= ")"; $query .= $values;
			$db_co->do($query);
			my $nutriments_id = $db_co->{ q{mysql_insertid}};
			# Insert product type

			# Insert Product
		}
	}

	# DB disconnection
	$db_co->disconnect();
}

##################### MAIN #####################
check_options();
if ( defined($o_help) ) { 
	help(); 
	exit 1; 
}
elsif ( !defined($o_source) 
		or !defined($o_db) 
		or !defined($o_user) 
		or !defined($o_passwd) ) {
	print_usage();
	exit 1;
}
else {
	get_products();
	import();
}
###

