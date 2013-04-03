#!/usr/bin/env perl

use strict;
use warnings;
use Getopt::Long;

########################################################
# Version : 1.0
# Date : Apr 03 2013
# Author : maxibgoode
########################################################


# Openfoodfacts.org API URL : complete with <productid>.json
use constant URL => "http://fr.openfoodfacts.org/api/v0/product/";

my $o_help = undef;
my $o_source = undef;
my $o_host = "localhost";
my $o_db = undef;
my $o_user = undef;
my $o_passwd = undef;



sub print_usage {
	print "Usage: $0 [-h|--help] -s|--source <data.csv> [-H|--host <db_hostname>] -d|--db <db_name> -u|--user <db_user> -p|--password <db_password>\n";
}

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

sub get_product_by_id {

}

sub import {

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
###


# GET example
#use LWP::Simple;
#my $json_produit = get($url);

