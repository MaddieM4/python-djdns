BIN=$(DESTDIR)/usr/bin
CONFDIR=$(DESTDIR)/etc/pymds
LIBDIR=$(DESTDIR)/usr/lib/pymds

all:

install:
	install -d $(BIN) $(LIBDIR)
	install -o root -g root -m 775 -d $(CONFDIR)
	install -m755 pymds $(BIN)
	install -m755 *.py $(LIBDIR)
