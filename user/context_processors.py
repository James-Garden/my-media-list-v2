def settings_nav_links(request):
    nav_links = {
        '/edit_profile': 'Profile',
        '/edit_account': 'Account',
    }
    return {'settings_nav_links': nav_links}
