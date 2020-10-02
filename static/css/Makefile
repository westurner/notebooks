
default: download checksums

download:
	wget https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css -O bootstrap.min.css


srihash=awk '{ print $$1 }' | xxd -r -p | base64

checksums:
	sha384sum bootstrap.min.css | ${srihash}
