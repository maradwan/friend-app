nginx:
  pkg.installed:
    - pkgs:
      - nginx-common
      - nginx-extras

  service:
    - running
    - watch:
      - file: /etc/nginx/*


/etc/nginx/sites-enabled/default:
  file.managed:
    - source: salt://nginx/files/default
    - template: jinja
    - user: root
    - group: root
    - mode: 0644
    - makedirs: True
    - defaults:
    - watch_in:
      - service: nginx

