# Server runtime third-party sources

This repository distributes upstream source and build material for third-party
components used by Bosonoo's server runtime images. It contains no Bosonoo
application source, customer data, credentials or deployment configuration.

## Source collections

- [Fedora 43 update of 1 October 2026](https://github.com/Bosonoo/server-runtime-sources/releases/tag/fedora43-20261001).
  The release asset `fedora43-20261001-sources.tar` contains one unmodified
  Fedora source RPM, `systemd-258.11-1.fc43`, totalling 17,461,158
  source-archive bytes. In Fedora 43 updates, it replaced `systemd-258.10-1.fc43`.
- [Fedora 43 collection of 26 September 2026](https://github.com/Bosonoo/server-runtime-sources/releases/tag/fedora43-20260926).
  The release asset `fedora43-20260926-sources.tar` contains 50 unmodified
  Fedora source RPMs, totalling 294,397,467 source-archive bytes.

Each source RPM contains its upstream sources, Fedora patches and RPM build
specification. [`source-index.json`](source-index.json) records exact versions,
upstream download URLs, build identifiers and hashes for the newest collection.
[`bundle.json`](bundle.json) identifies that complete bundle. An earlier
collection's index and `bundle.json` remain at its release tag; for example, see
[`fedora43-20260926`](https://github.com/Bosonoo/server-runtime-sources/tree/fedora43-20260926).
These sources were not modified by Bosonoo.

The collections include source for split binary packages from the same source
package. Inclusion here does not assert that every binary or optional component
is installed in a deployed image, or that a runtime release is qualified.
Runtime releases retain their own component inventory and notices.

## Verify and inspect

Download the source archive and this repository's `bundle.json`, then run:

```sh
python3 verify_bundle.py /path/to/fedora43-20261001-sources.tar
```

To verify an earlier collection, first check out its tag, such as
`git checkout fedora43-20260926`, then run the same command with that archive.

Verification reads the archive without executing or extracting its source. It
checks the complete bundle and every source RPM against the recorded SHA-256
hash and byte count, and rejects extra or duplicate archive members. After
verification, extract it into a new empty directory with your archive tool.

The distributed archives are the complete official unsigned Koji source RPMs.
Their compressed source payloads were checked against signed Fedora main
headers using the Fedora 43 signing key:
`C6E7F081CF80E13146676E88829B606631645531`.
The unsigned archive hashes and the signed payload/header hashes are distinct;
`source-index.json` records both. A checksum alone is not a signature.

## Build material

The `.spec` file inside each source RPM records its source inputs, patches,
build dependencies and configure/build/install instructions. Fedora's build
record is identified by `kojiBuildId` in the index. To rebuild a package in a
suitable Fedora development environment, for example:

```sh
mock -r fedora-43-x86_64 sources/systemd-258.11-1.fc43.src.rpm
```

See the [Mock project's documentation](https://rpm-software-management.github.io/mock/).
These instructions identify the supplied build machinery; they do not claim a
byte-for-byte reproduction with today's package repositories. Historical build
dependencies and toolchains can affect the resulting binary. No package source
or build script is executed by the download verification script.

## Licences and scope

Each third-party component retains its upstream licence, copyright and
notices, supplied within its source RPM. There is no single replacement licence
for the third-party collection. Source availability here does not impose that
component's licence on separate Bosonoo application code.

The small original documentation and verifier in this repository are MIT
licensed; see [LICENSE](LICENSE). That licence does not replace any upstream
component licence. Browser Blender source is maintained separately in
[blender-browser-runtime](https://github.com/Bosonoo/blender-browser-runtime).

This public download is available without sign-in or a source-access fee.
Source collections are versioned and retained; corrections receive a new
version instead of replacing source bytes at an existing release URL.
For a missing or inaccessible source archive, contact **admin@bosonoo.com**.
