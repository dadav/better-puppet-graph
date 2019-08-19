# The non-ssl virtual host
class { 'apache':
  default_vhost => false,
}
apache::vhost { 'mix.example.com non-ssl':
  servername   => 'mix.example.com',
  port         => '80',
  docroot      => '/var/www/mix',
  suphp_engine =>  "off",
}

# The SSL virtual host at the same domain
apache::vhost { 'mix.example.com ssl':
  servername => 'mix.example.com',
  port       => '443',
  docroot    => '/var/www/mix',
  ssl        => true,
  suphp_engine =>  "off",
}
