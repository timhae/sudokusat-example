with import <nixpkgs>{};

stdenv.mkDerivation rec {

    name = "sat";
    env = buildEnv {name = name; paths = buildInputs; };

    buildInputs = [ ]; 
    base = "/home/tim/master/sem2/sat/sudokusat-example/";
    shellHook = ''
mkdir -p /home/tim/vagrant2
cp ${base}Vagrantfile ${base}setup.sh /home/tim/vagrant2/
cd /home/tim/vagrant2
vagrant up
vagrant ssh
        '';
}
