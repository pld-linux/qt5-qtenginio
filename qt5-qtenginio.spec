#
# Conditional build:
%bcond_without	qch	# documentation in QCH format

%define		orgname		qtenginio
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Enginio library
Summary(pl.UTF-8):	Biblioteka Qt5 Enginio
Name:		qt5-%{orgname}
Version:	5.3.1
Release:	1
License:	LGPL v2.1 with Digia Qt LGPL Exception v1.1 or GPL v3.0
Group:		Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.3/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	89bffcd329886fd1fe4e504c666987cd
URL:		http://qt-project.org/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Sql-devel >= %{qtbase_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
%if %{with qch}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Enginio library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Enginio.

%package -n Qt5Enginio
Summary:	The Qt5 Enginio library
Summary(pl.UTF-8):	Biblioteka Qt5 Enginio
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Network >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}

%description -n Qt5Enginio
Qt5 Enginio is a client library for accessing Enginio service from Qt
and QML code.

%description -n Qt5Enginio -l pl.UTF-8
Biblioteka Qt5 Enginio to biblioteka kliencka służąca do dostępu do
usługi Enginio z poziomu Qt i QML-a.

%package -n Qt5Enginio-devel
Summary:	Qt5 Enginio library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Enginio - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Enginio = %{version}-%{release}
Requires:	Qt5Gui-devel >= %{qtbase_ver}
Requires:	Qt5Network-devel >= %{qtbase_ver}

%description -n Qt5Enginio-devel
Qt5 Enginio library - development files.

%description -n Qt5Enginio-devel -l pl.UTF-8
Biblioteka Qt5 Enginio - pliki programistyczne.

%package doc
Summary:	Qt5 Enginio documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Enginio w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 Enginio documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Enginio w formacie HTML.

%package doc-qch
Summary:	Qt5 Enginio documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Enginio w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 Enginio documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Enginio w formacie QCH.

%package examples
Summary:	Qt5 Enginio examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Enginio
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Qt5 Enginio examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Enginio.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{__make} %{!?with_qch:html_}docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_%{!?with_qch:html_}docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libEnginio.so.1.?
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libEnginio.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/enginio

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Enginio -p /sbin/ldconfig
%postun	-n Qt5Enginio -p /sbin/ldconfig

%files -n Qt5Enginio
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt README.md dist/changes-*
%attr(755,root,root) %{_libdir}/libEnginio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libEnginio.so.1
%dir %{qt5dir}/qml/Enginio
%attr(755,root,root) %{qt5dir}/qml/Enginio/libenginioplugin.so
%{qt5dir}/qml/Enginio/plugins.qmltypes
%{qt5dir}/qml/Enginio/qmldir

%files -n Qt5Enginio-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libEnginio.so
%{_libdir}/libEnginio.prl
%{_includedir}/qt5/Enginio
%{_pkgconfigdir}/Enginio.pc
%{_libdir}/cmake/Qt5Enginio
%{qt5dir}/mkspecs/modules/qt_lib_enginio.pri
%{qt5dir}/mkspecs/modules/qt_lib_enginio_private.pri

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtenginio
%{_docdir}/qt5-doc/qtenginiooverview
%{_docdir}/qt5-doc/qtenginioqml

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtenginio.qch
%{_docdir}/qt5-doc/qtenginiooverview.qch
%{_docdir}/qt5-doc/qtenginioqml.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
