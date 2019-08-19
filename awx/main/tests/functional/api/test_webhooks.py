import pytest

from awx.api.versioning import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_role, expect", [
        ('superuser', 200),
        ('org admin', 200),
        ('jt admin', 200),
        ('jt execute', 403),
        ('org member', 403),
    ]
)
def test_get_webhook_key_jt(organization_factory, job_template_factory, get, user_role, expect):
    objs = organization_factory("org", superusers=['admin'], users=['user'])
    jt = job_template_factory("jt", organization=objs.organization,
                              inventory='test_inv', project='test_proj').job_template
    if user_role == 'superuser':
        user = objs.superusers.admin
    else:
        user = objs.users.user
        grant_obj = objs.organization if user_role.startswith('org') else jt
        getattr(grant_obj, '{}_role'.format(user_role.split()[1])).members.add(user)

    url = reverse('api:webhook_key', kwargs={'model_kwarg': 'job_templates', 'pk': jt.pk})
    response = get(url, user=user)
    assert response.status_code == expect
    if expect < 400:
        assert response.data == {'webhook_key': ''}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_role, expect", [
        ('superuser', 200),
        ('org admin', 200),
        ('jt admin', 200),
        ('jt execute', 403),
        ('org member', 403),
    ]
)
def test_get_webhook_key_wfjt(organization_factory, workflow_job_template_factory, get, user_role, expect):
    objs = organization_factory("org", superusers=['admin'], users=['user'])
    wfjt = workflow_job_template_factory("wfjt", organization=objs.organization).workflow_job_template
    if user_role == 'superuser':
        user = objs.superusers.admin
    else:
        user = objs.users.user
        grant_obj = objs.organization if user_role.startswith('org') else wfjt
        getattr(grant_obj, '{}_role'.format(user_role.split()[1])).members.add(user)

    url = reverse('api:webhook_key', kwargs={'model_kwarg': 'workflow_job_templates', 'pk': wfjt.pk})
    response = get(url, user=user)
    assert response.status_code == expect
    if expect < 400:
        assert response.data == {'webhook_key': ''}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_role, expect", [
        ('superuser', 201),
        ('org admin', 201),
        ('jt admin', 201),
        ('jt execute', 403),
        ('org member', 403),
    ]
)
def test_post_webhook_key_jt(organization_factory, job_template_factory, post, user_role, expect):
    objs = organization_factory("org", superusers=['admin'], users=['user'])
    jt = job_template_factory("jt", organization=objs.organization,
                              inventory='test_inv', project='test_proj').job_template
    if user_role == 'superuser':
        user = objs.superusers.admin
    else:
        user = objs.users.user
        grant_obj = objs.organization if user_role.startswith('org') else jt
        getattr(grant_obj, '{}_role'.format(user_role.split()[1])).members.add(user)

    url = reverse('api:webhook_key', kwargs={'model_kwarg': 'job_templates', 'pk': jt.pk})
    response = post(url, {}, user=user)
    assert response.status_code == expect
    if expect < 400:
        assert bool(response.data.get('webhook_key'))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_role, expect", [
        ('superuser', 201),
        ('org admin', 201),
        ('jt admin', 201),
        ('jt execute', 403),
        ('org member', 403),
    ]
)
def test_post_webhook_key_wfjt(organization_factory, workflow_job_template_factory, post, user_role, expect):
    objs = organization_factory("org", superusers=['admin'], users=['user'])
    wfjt = workflow_job_template_factory("wfjt", organization=objs.organization).workflow_job_template
    if user_role == 'superuser':
        user = objs.superusers.admin
    else:
        user = objs.users.user
        grant_obj = objs.organization if user_role.startswith('org') else wfjt
        getattr(grant_obj, '{}_role'.format(user_role.split()[1])).members.add(user)

    url = reverse('api:webhook_key', kwargs={'model_kwarg': 'workflow_job_templates', 'pk': wfjt.pk})
    response = post(url, {}, user=user)
    assert response.status_code == expect
    if expect < 400:
        assert bool(response.data.get('webhook_key'))
