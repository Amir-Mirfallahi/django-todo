{% extends "mail_templated/base.tpl" %}

{% block subject %}
Confirmation Email
{% endblock %}

{% block html %}
Here is your token:
<a href="http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{ token }}">Activate your account</a>
{% endblock %}