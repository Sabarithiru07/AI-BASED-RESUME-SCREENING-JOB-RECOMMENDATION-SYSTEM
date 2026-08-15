def notifications_count(request):
    """Inject unread notification count and user role into every template context."""
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()

        # Safely resolve role - superuser may have no UserProfile row
        if request.user.is_superuser:
            role = 'admin'
            role_display = 'Admin'
        else:
            try:
                profile = request.user.profile
                role = profile.role
                role_display = profile.get_role_display()
            except Exception:
                role = 'user'
                role_display = 'Job Seeker'

        return {
            'unread_notifications_count': count,
            'user_role': role,
            'user_role_display': role_display,
        }
    return {
        'unread_notifications_count': 0,
        'user_role': '',
        'user_role_display': '',
    }
