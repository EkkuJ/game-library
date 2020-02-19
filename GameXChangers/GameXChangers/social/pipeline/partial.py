from social_core.pipeline.partial import partial
from django.contrib.auth.models import Group
from django.http import HttpResponseNotFound

def is_in_group(user):
    res = (user.groups.filter(name='Developer').exists() or
        user.groups.filter(name='Player').exists())
    return res

@partial
def save_user(strategy, details, request, user=None, *args, **kwargs):

    if is_in_group(user):
        return {'is_new': False}

    group = strategy.session_get('group',None)
    if group is None or group == 'None':
        current_partial = kwargs.get('current_partial')
        return strategy.redirect(
            '/authentication/group?partial_token={0}'.format(current_partial.token)
        )
    else:
        HttpResponseNotFound()
    
    profile = user
    
    if group == 'developer':
        developers = Group.objects.get(name='Developer')
        user.groups.add(developers)
    elif group == 'player':
        players = Group.objects.get(name='Player')
        user.groups.add(players)
    else: 
        return HttpResponseNotFound(str(group))
    
    profile.save()

    return