{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset Password
{% endblock %}

{% block html %}
Click on this button to reset your password:

<a href="http://127.0.0.1:8000/accounts/api/v1/reset-password-confirm/{{ token }}">Reset Password</a>
{% endblock %}