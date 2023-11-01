%bcond_without check

%if ! 0%{?gobuild:1}
%define gobuild(o:) \
GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -linkmode=external -compressdwarf=false -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v %{?**};
%endif

%global commit0 d97078115282836e16d0dca10b4b42ce60fc70e6
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name: golang-github-cpuguy83-md2man
Version: 2.0.2
Release: 4%{?dist}
Summary: Converts markdown into roff (man pages)
License: MIT
URL: https://github.com/cpuguy83/go-md2man
Source0: https://github.com/cpuguy83/go-md2man/archive/%{commit0}/%{name}-%{version}-%{shortcommit0}.tar.gz
# https://fedoraproject.org/wiki/PackagingDrafts/Go#Go_Language_Architectures
ExclusiveArch: %{go_arches}
BuildRequires: golang
BuildRequires: git-core
Provides: go-md2man = %{version}-%{release}

%description
Converts markdown into roff (man pages).

%prep
%autosetup -Sgit -n go-md2man-%{commit0}

%build
ln -s vendor src
mkdir -p src/github.com/cpuguy83
ln -s $(pwd) src/github.com/cpuguy83/go-md2man
export GO111MODULE=off
export GOPATH=$(pwd)
export CGO_CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
%ifarch x86_64
export CGO_CFLAGS+=" -fcf-protection=full"
%endif
GOPATH=$GOPATH %gobuild -o bin/go-md2man github.com/cpuguy83/go-md2man

%install
install -m 0755 -vd %{buildroot}%{_bindir}
install -m 0755 -vp bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%endif

%files
%license LICENSE.md
%doc README.md go-md2man.1.md
%{_bindir}/*

%changelog
* Fri Dec 02 2022 Jindrich Novy <jnovy@redhat.com> - 2.0.2-4
- fix RHEL9.2 build - thanks to Debarshi Ray
- Related: #2124478

* Tue Nov 29 2022 Jindrich Novy <jnovy@redhat.com> - 2.0.2-3
- rebuild
- Resolves: #2037812

* Thu Aug 04 2022 Jindrich Novy <jnovy@redhat.com> - 2.0.2-2
- limit to golang arches only
- Related: #2061316

* Thu Aug 04 2022 Jindrich Novy <jnovy@redhat.com>
- update to 2.0.2
- Related: #2061316

* Thu Feb 17 2022 Jindrich Novy <jnovy@redhat.com> - 2.0.0-18.gitaf8da76
- fix gating.yaml as we have no functional gating tests
- Related: #2000051

* Wed Feb 16 2022 Jindrich Novy <jnovy@redhat.com> - 2.0.0-17.gitaf8da76
- update gating.yaml and rebuild
- Related: #2000051

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 2.0.0-16.gitaf8da76
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Jul 15 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-15.gitaf8da76
- Resolves: #1975362 - enable additional hardening flags

* Tue Jul 13 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-14.gitaf8da76
- Resolves: #1975362 - enable full cf-protection for x86_64

* Mon Jul 12 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-13.gitaf8da76
- Resolves: #1975362 - use latest upstream commit

* Fri Jul 09 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-12
- Resolves: #1975362 - add -fcf-protection to CGO_CFLAGS

* Thu Jul 08 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-11
- Resolves: #1975362 - add gating.yaml

* Thu Jul 08 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-10
- Resolves: #1975362 - build with CGO_CFLAGS defined

* Tue Jul 06 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-9
- Resolves: #1975362 - rebuild with explicit git-core dep

* Wed Jun 23 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-8
- Resolves: #1975362 - fix gobuild issues

* Tue Jun 22 2021 Mohan Boddu <mboddu@redhat.com> - 2.0.0-7
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Mon Jun 21 2021 Lokesh Mandvekar <lsm5@redhat.com> - 2.0.0-6
- Resolves: #1974463 - build with vendored sources to reduce package set

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 2.0.0-5.gitaf8da76
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 09 2021 Robert-André Mauchin <zebob.m@gmail.com> - 2.0.0-3.20210109gitaf8da76
- Bump to commit af8da765f0460ccb1d91003b4945a792363a94ca

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 25 19:30:39 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2.0.0-1.20200725git1029f53
- Bump to commit 1029f53b6507e27158d89cd489669559c1c700a3

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 05 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.0.0-0.3.20190624gitf79a8a8
- Add Obsoletes for old name

* Thu Jun 27 18:13:22 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 2.0.0-0.2.20190624gitf79a8a8
- Add Provides

* Thu Apr 25 17:25:58 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 2.0.0-0.1.20190624gitf79a8a8
- Prerelease 2.0.0, bump to commit f79a8a8ca69da163eee19ab442bedad7a35bba5a

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 25 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.8-2
- Replace blackfriday import path

* Thu Oct 25 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.8-1
- Update to release v1.0.8

* Tue Oct 23 2018 Nicolas Mailhot <nim@fedoraproject.org> - 1.0.7-9
- redhat-rpm-config-123 triggers bugs in gosetup, remove it from Go spec files as it’s just an alias
- https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/RWD5YATAYAFWKIDZBB7EB6N5DAO4ZKFM/

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1.0.7-8
- Rebuild with fixed binutils

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-7.20180312git1d903dc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 09 2018 Jan Chaloupka <jchaloup@redhat.com> - 1.0.7-6.20180312git1d903dc
- Upload glide file

* Wed Mar 07 2018 Jan Chaloupka <jchaloup@redhat.com> - 1.0.7-5.git1d903dc
- Fix go vet warning: Fatal -> Fatalf

* Wed Feb 28 2018 Jan Chaloupka <jchaloup@redhat.com>
- Autogenerate some parts using the new macros

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.7-3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 19 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.0.7-1
- Bump to upstream 1d903dcb749992f3741d744c0f8376b4bd7eb3e1
  related: #1222796

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 14 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.0.4-7
- Bump to upstream a65d4d2de4d5f7c74868dfa9b202a3c8be315aaa
  related: #1222796

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- https://fedoraproject.org/wiki/Changes/golang1.7

* Sun Mar 06 2016 jchaloup <jchaloup@redhat.com> - 1.0.4-4
- Update list of provided packages
  resolves: #1222796

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- https://fedoraproject.org/wiki/Changes/golang1.6

* Thu Sep 10 2015 jchaloup <jchaloup@redhat.com> - 1-13
- Generate man page as well
  related: #1222796

* Sun Aug 30 2015 jchaloup <jchaloup@redhat.com> - 1-12
- Change deps on compiler(go-compiler)
- Update %%build, %%test and main section accordingaly
  related: #1222796

* Sat Aug 29 2015 jchaloup <jchaloup@redhat.com> - 1-11
- Reduce build section after update of go-srpm-macros
- BUILD_ID for debug is needed only for golang compiler
  related: #1222796

* Tue Aug 25 2015 jchaloup <jchaloup@redhat.com> - 1-10
- Provide devel package on rhel7
  related: #1222796

* Thu Aug 20 2015 jchaloup <jchaloup@redhat.com> - 1-9
- Update spec file to spec-2.0
  related: #1222796

* Mon Jul 20 2015 jchaloup <jchaloup@redhat.com> - 1-8
- Add with_* macros

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 jchaloup <jchaloup@redhat.com> - 1-6
- Remove runtime deps of devel on golang
- Polish spec file
  related: #1222796

* Sun May 17 2015 jchaloup <jchaloup@redhat.com> - 1-5
- Add debug info
- Add license
- Update spec file to build on secondary architectures as well
  related: #1222796

* Wed Feb 25 2015 jchaloup <jchaloup@redhat.com> - 1-4
- Bump to upstream 2831f11f66ff4008f10e2cd7ed9a85e3d3fc2bed
  related: #1156492

* Wed Feb 25 2015 jchaloup <jchaloup@redhat.com> - 1-3
- Add commit and shortcommit global variable
  related: #1156492

* Mon Oct 27 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1-2
- Resolves: rhbz#1156492 - initial fedora upload
- quiet setup
- no test files, disable check

* Thu Sep 11 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1-1
- Initial package
