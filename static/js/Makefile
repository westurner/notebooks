
default: download checksums

download:
	wget "https://code.jquery.com/jquery-3.5.1.slim.min.js" -O jquery-3.5.1.slim.min.js
	wget "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" -O popper.min.js
	wget "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" -O bootstrap.min.js

srihash=awk '{ print $$1 }' | xxd -r -p | base64

checksums:
	sha384sum jquery-3.5.1.slim.min.js | ${srihash}
	sha384sum popper.min.js | ${srihash}
	sha384sum bootstrap.min.js | ${srihash}
