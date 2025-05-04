{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-unstable.tar.gz") {} }:

pkgs.mkShell {
    buildInputs = with pkgs; [
        python313
        python313Packages.pip
        python313Packages.pip-tools
    ];

    shellHook = ''
        # Create and activate virtual environment if it doesn't exist
        VENV=.venv
        if [ ! -d "$VENV" ]; then
            python -m venv $VENV
        fi
        source $VENV/bin/activate

        # Install or update dependencies
        pip install -r requirements.txt || echo "No requirements.txt found"

        # Shell aliases
        alias compile-requirements="pip-compile requirements.in -o requirements.txt"
        alias upgrade-requirements="pip-compile requirements.in -o requirements.txt --upgrade"

        echo "--------------------------------"
        echo "Shell aliases available:"
        echo "  compile-requirements: Recompile requirements.in to requirements.txt"
        echo "  upgrade-requirements: Upgrade and recompile all packages in requirements.txt"
    '';
}
