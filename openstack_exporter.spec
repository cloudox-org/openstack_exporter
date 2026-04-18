%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name: openstack_exporter
Version: 1.7.0
Release: 1%{?dist}
Summary: Prometheus exporter for OpenStack metrics.
License: MIT
URL:     https://github.com/openstack-exporter/openstack-exporter

Source0: https://github.com/openstack-exporter/openstack-exporter/releases/download/v%{version}/openstack-exporter_%{version}_linux_amd64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default
Source3: %{name}_clouds.yaml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
OpenStack exporter for Prometheus written in Golang using the gophercloud library.

%prep
%setup -q -D -c openstack-exporter_%{version}_linux_amd64
mv -v openstack-exporter %{name}

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{name}_clouds.yaml

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service
%config(noreplace) %attr(640, -, %{group})%{_sysconfdir}/prometheus/%{name}_clouds.yaml

%changelog
* Sat Apr 18 2026 Ivan Garcia <igarcia@cloudox.org> - 1.7.0
- Initial packaging for the 1.7.0 branch
