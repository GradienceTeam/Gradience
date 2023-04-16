{
  description = "Gradience";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/unstable";
    
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, ... }@inputs: inputs.utils.lib.eachSystem [
    "x86_64-linux" "aarch64-linux"
  ] (system: let pkgs = import nixpkgs { inherit system; };
  in {

    # This block here is used when running `nix develop`
    devShells.default = pkgs.mkShell rec {
      # Update the name to something that suites your project.
      name = "gradience";

      python = with pkgs.python3Packages; [
        anyascii
        jinja2
        lxml
        material-color-utilities
        pygobject3
        svglib
        yapsy
      ];

      # build environment dependencies
      packages = with pkgs; [
        appstream-glib
        blueprint-compiler
        desktop-file-utils
        gettext
        glib
        gobject-introspection
        meson
        ninja
        pkg-config
        wrapGAppsHook4
        sassc
        libadwaita
        libportal
        libportal-gtk4
        librsvg
        libsoup_3
      ] ++ python;


    };

    # This is used when running `nix build`
    packages.default = pkgs.llvmPackages_14.stdenv.mkDerivation rec {
      name = "worm";
      version = "0.1.1";
  
      src = self;

      buildInputs = [ pkgs.ncurses6 ];

      buildPhase = "COMPILER='clang++' make";

      installPhase = ''
        mkdir -p $out/bin; 
        install -t $out/bin worm
      '';

      meta = with inputs.utils.lib; {
        homepage = "https://github.com/icecreammatt/ssu-cs315-worm";
        description = ''
          Terminal CLI Worm Game
        '';
      };
    };
   
  });
}