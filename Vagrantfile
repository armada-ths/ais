# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "aisbox"
  config.vm.define "aisbox"
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  config.vm.provision :shell,
    path: "scripts/vagrant/provision.sh",
    privileged: false
  config.vm.provision :shell,
    path: "scripts/vagrant/up.sh",
    privileged: false,
    run: "always"
end
