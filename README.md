# python-DJDNS

This is a DJDNS server written in Python. It is a Decentralized DNS server for a more secure, free internet.

Right now none of the P2P magic works or is used, due to the so-called "bootstrapping issue" in DEJE.All the data is fed from on-disk files that would normally be hosted in DEJE. The positive side is that you can install a DJDNS server in its current demo state without installing as much extra crap as dependencies.

A nifty feature of DJDNS is how handy it is at deferal. It uses public servers to flexibly resolve ICANN, Namecoin, and OpenNIC records, with more alternative DNS deferals to come. Just make an issue [in djdns-flat-hype][dhf] for your favorite(s), and I'll go about adding support! Same goes for personal domains - make an issue or a pull request, and I'll probably get it merged, as long as it's not too contentious.

## Try out the public alpha now!

I'm running a server on roaming-initiative.com for people to use on and off the meshnet. To use it:

### Back up your existing conf

If something goes terribly wrong, whether on your end or mine, you'll want to have your old config back. So in your shell, do this:

    $ cp /etc/resolv.conf /etc/resolv.conf.bak

Or more succinctly (although I think it's specific to bash):

    $ cp /etc/resolv.conf{,.bak}

That way, you can copy the original back over later if you have to.

### Put in the new conf

Replace the contents of /etc/resolv.conf with the following:

    nameserver [fcd5:7d07:2146:f18f:f937:d46e:77c9:80e7]
    nameserver 173.255.210.202
    nameserver 8.8.8.8

These are, respectively:

 * Roaming Initiative on Hyperboria.
 * Roaming Initiative via IPv4 Clearnet.
 * Google Public DNS.

This should be a pretty sane chain of fallbacks for most alpha testers, but don't be afraid to mix things up and experiment if you feel like it. That's what config backups are for!

### Report any issues here on Github

This project uses the Github issue tracker. If you don't use GH and don't intend to, you can email me at philip@roaming-initiative.com, or find me on HypeIRC.

# Production installation

This is the new and vastly simpler system for installing DJDNS in a production environment on your own server. All you need to do to install and start DJDNS, such that it starts immediately and on reboots, and is controllable through /etc/init.d/djdns?

```bash
$ git clone https://github.com/campadrenalin/python-djdns
$ sudo python-djdns/scripts/install.sh
```

Now, in another terminal or tab or whatever, you should be able to hit that running server with DNS requests using the program 'dig' (you may need to install the dnsutils package).

```bash
$ dig @localhost google.com
$ dig @localhost ri.hype
$ dig @localhost dot-bit.bit
```

This automatically downloads and uses [djdns-hype-flat][dhf] as the source data. DJDNS production installations will serve based on whatever is in /var/dns/data, so it's easy to use a different page repo if you want.

If this does not work, we now include a debug wrapper that allows you to run djdns within the terminal, instead of as a daemon, using the system virtualenv and /var/dns/data. This is great for quickly diagnosing why djdns doesn't start. And the wrapper script is installed into a handy location, too.

    $ sudo djdns

## Updating DJDNS

When DJDNS or your source data has an update, you can apply it with the update.sh script in the scripts folder. This must be run as root.

```bash
$ cd python-djdns
$ git pull # Not done automatically by update script
$ sudo scripts/update.sh
```

This should even work seamlessly for alternative data directories as long as they are git repositories, such that 'git pull' will bring the data up-to-date.

## Uninstalling DJDNS

All global stuff installation stuff will be cleaned up if you run:

    $ sudo ./scripts/uninstall.sh

This will stop the service if it's running, remove installed files, etc.

# Development setup

You can set up a virtualenv within or outside the cloned repo, and install DJDNS into it manually.

```bash
$ virtualenv testenv
$ . testenv/bin/activate
$ pip install -r requirements.txt
$ python setup.py install
```
 
This test environment will have the djdns script in its $PATH. So you can run the server like this, whenever you are "activated" into the venv:

```bash
$ djdns -d diskdemo -p 9999 -u $USER -g $USER
```

You should then be able to query the server (in another terminal) at the given port, for the domains defined in the diskdemo directory. Feel free to explore and play with its contents to gain a basic understanding of how the page structure works.

```bash
$ dig @localhost -p 8989 in.root.demo       # 1.2.3.4
$ dig @localhost -p 8989 in.subbranch.demo  # 5.5.5.5
$ dig @localhost -p 8989 in.b3.demo         # 5.6.7.8
```

For further reference on the specification, see [this Github comment](https://github.com/campadrenalin/python-djdns/issues/2#issuecomment-18111938).

It is possible to run a test environ on port 53, but it's awkward and awful. Don't do it.

# About DJDNS

## Decentralized DNS is cool.

Which is why I'm building a version on top of the DEJE library. The DEJE platform provides security,
authentication, democratic management, and psychotic levels of cacheability.

## How resistant is this system to tampering?

DJDNS is based on a hierarchy of DEJE documents. Each can store references to other documents, based on regexes.
For example, "You can find out about all \*.hype domains over here in this other place." Each page can hold
arbitrary data, so that DJDNS will be forward-compatible, but a few types of data will be understood in very
early versions: domain resolution information, domain ownership information (WHOIS), and EJTP identities. After
that, it'll probably be used to replace the existing certificate system used by SSL, but that's down the road
aways.

The system is cryptographically secure such that you can verify the entire chain of operations given a known
accurate previous state. If someone tries to send you false information, your DJDNS implementation will not
only notice that you're being lied to, but start trying alternate sources of information to find a truthful one.
Control over who can edit a document is fully customizable, and designed to strike an ideal balance between
permissive areas and privately controlled areas, and between automation and personal approval.

### What about Sybil attacks? What is the policy for new domains?

The problem summarrized in this question is one that most decentralized DNS implementations struggle with. What
is the "price" of a domain registration? In namecoin, it's a bitcoin value, so money basically. With the more
loose web-of-trust approaches, registry space truly is infinite since the system doesn't concern itself with
name collisions except to pick the most personally algorithmically trusted contender in the collision. Some systems
propose rate limiting, but this is very easy to defeat with Sybil attacks - a strategy named after a famous
psychiatric case study of a woman with multiple personality disorder, in which the attacker uses a multitude of
distinct personas (stolen, or generated mechanically or by hand) to defeat "one per customer" sorta limits.

DJDNS takes an entirely different approach that I like to call recursive democracy, which averts such problems 
altogether, by not establishing a "global policy" per se at all, except in the most fundamentally basic and
democratic terms. As stated earlier in the readme, every page represents a subdomain (except the TLD page, if you
want to be technical and pedantic about it). Each page can have any kind of custom rules for moderation and
modification of its contents. The TLD can be administrated by a voting consensus of hundreds of thousands of
people. Your site page can be administrated by your web dude.

Some pages will use automatic approval (domain follows specific rules and isn't taken? Add it to the list!),
others will use manual (must be approved by some critical mass of moderators), some will use a combination.
The price of a domain is just convincing a system or group of people to point a delegation regex to your
DJDNS document.

## And there's no name collisions... ever?

Right. It's not like WOT, where it will try to guess the best known option based on who you personally trust. It's a
community-managed ecosystem with fine-grained syncronization controls and configurability. Everybody's on the
"same page", so to speak, only storing and managing the parts they have interest in. The worst you can possibly do
is get an out-of-date copy, which will store enough participant references that you can ask around and make sure you
have the most recent copy.

## Is this a high-bandwidth thing?

Depends on what pages you're hosting, and how many people are hitting your server with DNS requests. But generally,
no, fairly low-bandwidth EJTP stuff.

## Are there any downsides?

Some specific documents may be bandwidth- or disk-intensive, like the TLD.

## How close is this to completion?

I have a public server running the alpha version, which is buggy but surprisingly usable. It uses [flat files][dhf] instead of DEJE documents, which will change when DEJE becomes mature enough.

It is also easy to set up your own public server, as that's basically an automated process now. If you want to publicly serve via DJDNS, *it is not hard.*

I have a fairly well-defined roadmap from here, in terms of tasks. A bunch of small bugfixes and features and such, and one big important project (switch to DEJE) looming in the future. The only thing I don't know is the timetable. It'll be ready when it's ready.

## Is this anything like CJDNS?

No, and the confusion is mostly on the part of CJD for naming his really cool software in a really misleading way. CJDNS
stands for CJD's Networking Suite, and doesn't do DNS at all. DJDNS stands for DEJE DNS, and DNS is all it does.
You can think of it as *CJD NS* vs *DJ DNS*.

[dhf]: https://github.com/campadrenalin/djdns-hype-flat
