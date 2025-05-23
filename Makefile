# This is a catch all for cleaning up any old bytecode, rebuilding the bytecode and packaging both a zipapp and source distributions
all: clean bytecode package source

binary:
	@mkdir -p dist/
	@nuitka --onefile src/__main__.py
	@rm -rf __main__.build/
	@rm -rf __main__.dist/
	@rm -rf __main__.onefile-build/
	@mv __main__.bin dist/hs

# Build the bytecode only
bytecode:
	@python3 -m compileall -qq src

# Clean up any old bytecode
clean:
	@rm -rf dist/
	@rm -rf ./src/__pycache__/
	@rm -rf ./src/etc/__pycache__/
	@rm -rf ./src/maple/__pycache__/
	@rm -rf ./src/interpreter/__pycache__/
	@rm -rf ./src/maple/error/__pycache__/
	@rm -rf ./src/statements/__pycache__/
	@rm -rf ./src/tools/__pycache__/
	@rm -rf ./tests/__pycache__/

	@rm -rf ./src/.ruff_cache/
	@rm -rf ./src/etc/.ruff_cache/
	@rm -rf ./src/maple/.ruff_cache/
	@rm -rf ./src/interpreter/.ruff_cache/
	@rm -rf ./src/maple/error/.ruff_cache/
	@rm -rf ./src/statements/.ruff_cache/
	@rm -rf ./src/tools/.ruff_cache/
	@rm -rf ./tests/.ruff_cache/

# Install Helasuno to /usr/local/bin/
install: dist/hs
	@cp dist/hs /usr/local/bin/
	@chmod 755 /usr/local/bin/hs
	@chmod +x /usr/local/bin/hs

package:
	@mkdir -p dist/
	@python3 package.py

# Make source based distributions in the form of tarballs and zip files
source:
	@mkdir -p dist/
	@tar -cjf dist/helasuno.tar.bz2 src
	@zip -r -q dist/helasuno.zip src

# Uninstall the interpreter if it's been installed.
uninstall:
	@rm -f /usr/local/bin/hs