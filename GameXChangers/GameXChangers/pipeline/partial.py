from social_core.pipeline.partial import partial
from django.contrib.auth.models import Group


@partial
def save_user(strategy, user, *args, **kwargs):

    group = strategy.session_get('group', None)
    if not group:
        return strategy.redirect('/authentication/group')

    profile = user
    
    if group == 'developer':
        developers = Group.objects.get(name='Developer')
        user.groups.add(developers)
    else:
        players = Group.objects.get(name='Player')
        user.groups.add(players)
    
    profile.save()

    return