#!/usr/bin/php
<?php
define( 'ABS_PATH', '/usr/share/wordpress/');
define( 'WP_INSTALLING', true );

/** Load WordPress Bootstrap */
require_once('/usr/share/wordpress/wp-load.php' );

/** Load WordPress Administration Upgrade API */
require_once('/usr/share/wordpress/wp-admin/includes/upgrade.php' );

/** Load wpdb */
require_once('/usr/share/wordpress/wp-includes/wp-db.php');

// Let's check to make sure WP isn't already installed.
if ( is_blog_installed() ) {
	die( 'Already Installed');
}

$php_version    = phpversion();
$mysql_version  = $wpdb->db_version();
$php_compat     = version_compare( $php_version, $required_php_version, '>=' );
$mysql_compat   = version_compare( $mysql_version, $required_mysql_version, '>=' ) || file_exists( WP_CONTENT_DIR . '/db.php' );

if ( !$mysql_compat && !$php_compat )
	$compat = sprintf( __('You cannot install because <a href="http://codex.wordpress.org/Version_%1$s">WordPress %1$s</a> requires PHP version %2$s or higher and MySQL version %3$s or higher. You are running PHP version %4$s and MySQL version %5$s.'), $wp_version, $required_php_version, $required_mysql_version, $php_version, $mysql_version );
elseif ( !$php_compat )
	$compat = sprintf( __('You cannot install because <a href="http://codex.wordpress.org/Version_%1$s">WordPress %1$s</a> requires PHP version %2$s or higher. You are running version %3$s.'), $wp_version, $required_php_version, $php_version );
elseif ( !$mysql_compat )
	$compat = sprintf( __('You cannot install because <a href="http://codex.wordpress.org/Version_%1$s">WordPress %1$s</a> requires MySQL version %2$s or higher. You are running version %3$s.'), $wp_version, $required_mysql_version, $mysql_version );

if ( !$mysql_compat || !$php_compat ) {
	display_header();
	die('<h1>' . __('Insufficient Requirements') . '</h1><p>' . $compat . '</p></body></html>');
}

$result = wp_install("${wp_blog_title}", "${wp_admin_username}", "${wp_admin_email}", false, '', "${wp_admin_password}");
extract( $result, EXTR_SKIP );

echo 'WordPress has been installed. Were you expecting more steps? Sorry to disappoint.';
