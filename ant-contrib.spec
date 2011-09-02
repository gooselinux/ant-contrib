%define beta_number b2

Summary:        Collection of tasks for Ant
Name:           ant-contrib
Version:        1.0
Release:        0.10.%{beta_number}%{?dist}
License:        ASL 2.0
URL:            http://ant-contrib.sourceforge.net/
Group:          Development/Libraries
Source0:        http://prdownloads.sourceforge.net/ant-contrib/ant-contrib-%{version}%{beta_number}-src.tar.gz
Patch0:         ant-contrib-build_xml.patch
Patch2:         ant-contrib-antservertest.patch
BuildRequires:  jpackage-utils >= 1.5
BuildRequires:  junit >= 3.8.0
BuildRequires:  ant-junit >= 1.6.2
BuildRequires:  ant-nodeps >= 1.6.2
BuildRequires:  xerces-j2
BuildRequires:  bcel >= 5.0
BuildRequires:  java-devel >= 1.4.2
Requires:       java >= 1.4.2
Requires:       junit >= 3.8.0
Requires:       ant >= 1.6.2
Requires:       xerces-j2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
The Ant-Contrib project is a collection of tasks
(and at one point maybe types and other tools)
for Apache Ant.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description    javadoc
Api documentation for %{name}.

%prep
%setup -q  -n %{name}
rm -rf test/src/net/sf/antcontrib/antclipse

%patch0
%patch2
sed -i "s/\r//" manual/tasks/foreach.html manual/tasks/for.html

%build
export JUNIT_VER=`rpm -q --queryformat='%%{version}' junit`
mkdir -p test/lib
(cd test/lib
ln -s $(find-jar junit-$(JUNIT_VER)) junit-$(JUNIT_VER).jar
)
export OPT_JAR_LIST="ant/ant-junit junit ant/ant-nodeps"
export CLASSPATH=
CLASSPATH=build/lib/ant-contrib-%{version}.jar:$CLASSPATH
echo $ANT_HOME
ant -Dsource=1.4 -Dversion=%{version} -Dbcel.jar=file://%{_javadir}/bcel.jar all

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -Dpm 644 build/lib/%{name}.jar \
      $RPM_BUILD_ROOT%{_javadir}/ant/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/ant/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
rm -rf build/docs/api

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "ant/ant-contrib" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/ant-contrib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/ant.d/ant-contrib
%{_javadir}/ant/*.jar
%doc build/docs/LICENSE.txt
%doc build/docs/tasks/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

%changelog
* Fri Sep 4 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.10.b2
- Install ant contrib in ant.d.

* Fri Sep 4 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.9.b2
- Drop gcj_support.
- Install as proper ant plugin.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.7.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-0.6.b2
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-0.5.b2
- Autorebuild for GCC 4.3

* Sun Aug 03 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.4.b2
- Added dist tag to release.

* Sat Aug 02 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.3.b2
- Removed unneccessary 0 epoch from required packages.
- Fixed dependance on specifically version 3.8.1 of junit.

* Tue Jun 27 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.2.b2
- Removed Class-Path from ant-contrib.jar file.
- Renamed patches.

* Tue Jun 27 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.1.b2
- Fixed release number to reflect beta status
- Removed Distribution and Vendor tags
- Fixed duplication in postun section
- Removed patch3, and used sed to fix line-endings instead

* Tue Jun 27 2006 Igor Foox <ifoox@redhat.com> - 1.0-1.b2
- Changed release-version to comply with FE standards
- Consolidated into -manual into main package
- Removed ghosting of the manual symlink
- Removed Epoch
- Run dos2unix over some manual files that have windows line endings
- Changed group for docs to Documentation
- Remove unused Source1
- Set Source0 to valid URL instead of just a file name
- Fix indentation
- Remove {push,pop}d and -c from %%setup
- Changed %%defattr in the %%files section to standard (-,root,root,-)

* Thu Jun 1 2006 Igor Foox <ifoox@redhat.com> - 0:1.0b2-1jpp_1fc
- Update to version 1.0b2
- Added native compilation
- Changed BuildRoot to what Extras expects

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.6-4jpp
- Upgrade to ant-1.6.2
- BuildReq/Req ant = 0:1.6.2
- Relax some other requirements

* Thu Jun 03 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.6-3jpp
- Fix missing buildrequires

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:0.6-2jpp
- Upgrade to Ant 1.6.X

* Wed Mar 24 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.6-1jpp
- First JPackage release
