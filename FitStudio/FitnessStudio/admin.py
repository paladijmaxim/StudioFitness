from django.contrib import admin
from django.utils.html import mark_safe
from .models import User, Tariff, Club, UserMembership, Payment, Class, Trainer, Event, Booking, Trainer_club

class UserMembershipInline(admin.TabularInline):
    model = UserMembership
    extra = 1
    classes = ('collapse',)
    raw_id_fields = ('tariff_id', 'club_id')
    readonly_fields = ('created_at',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    classes = ('collapse',)
    raw_id_fields = ('user_membership_id',)
    readonly_fields = ('created_at',)

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 1
    classes = ('collapse',)
    raw_id_fields = ('event_id',)
    readonly_fields = ('created_at',)

class TrainerClubInline(admin.TabularInline):
    model = Trainer_club
    extra = 1
    classes = ('collapse',)
    raw_id_fields = ('club_id',)

class EventInline(admin.TabularInline):
    model = Event
    extra = 1
    classes = ('collapse',)
    raw_id_fields = ('class_id', 'trainer_id')
    readonly_fields = ('booked_count',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'phone', 'created_at')
    list_filter = ('username', 'created_at',)
    search_fields = ('username', 'email')
    date_hierarchy = 'created_at'
    list_display_links = ('username', 'email')
    raw_id_fields = ('groups', 'user_permissions')
    readonly_fields = ('created_at', 'last_login', 'date_joined')
    filter_horizontal = ('groups', 'user_permissions')
    inlines = [UserMembershipInline, PaymentInline, BookingInline]
    @admin.display(description='Full Name')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.second_name}"
    @admin.display(description='Memberships')
    def membership_count(self, obj):
        return obj.memberships.count()


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'tariff_id', 'club_id', 'start_date', 'end_date', 'status', 'is_active',
                    'days_remaining', 'created_at')
    list_display_links = ('user_id', 'tariff_id')
    list_filter = ('status', 'tariff_id', 'club_id', 'created_at')
    search_fields = ('user_id__username', 'user_id__first_name', 'tariff_id__name', 'club_id__name')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user_id', 'tariff_id', 'club_id')
    readonly_fields = ('created_at',)

    @admin.display(description='Active', boolean=True)
    def is_active(self, obj):
        from django.utils import timezone
        return obj.status == 'active' and obj.end_date > timezone.now()

    @admin.display(description='Days Left')
    def days_remaining(self, obj):
        from django.utils import timezone
        if obj.end_date:
            remaining = (obj.end_date - timezone.now()).days
            return max(0, remaining)
        return 0
    def days_remaining_display(self, obj):
        days = self.days_remaining(obj)
        return f"{days} days"
    days_remaining_display.short_description = 'Days Remaining'
    readonly_fields = ('created_at', 'days_remaining_display')


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone')
    search_fields = ('name', 'address', 'phone')
    list_filter = ('name', 'address', 'phone')
    list_display_links = ('name',)
    inlines = [TrainerClubInline, EventInline]
    @admin.display(description='Address')
    def address_short(self, obj):
        return obj.address[:50] + '...' if len(obj.address) > 50 else obj.address
    @admin.display(description='Trainers')
    def trainers_count(self, obj):
        return obj.trainer_clubs.filter(is_active=True).count()
    @admin.display(description='Events')
    def events_count(self, obj):
        return obj.events.count()

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price_per_month', 'is_active')
    search_fields = ('name', 'price_per_month')
    list_display_links = ('name',)
    list_filter = ('is_active', 'price_per_month')
    readonly_fields = ('created_display',)
    @admin.display(description='Active Members')
    def active_memberships(self, obj):
        return obj.memberships.filter(status='active').count()
    def created_display(self, obj):
        return "System tariff"
    created_display.short_description = 'Type'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'user_membership_id', 'amount', 'created_at')
    search_fields = ('user_id__username', 'user_membership_id__id')
    list_display_links = ('user_id', 'user_membership_id')
    list_filter = ('status', 'created_at')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user_id', 'user_membership_id')
    readonly_fields = ('created_at', 'status_display')
    @admin.display(description='Status', boolean=True)
    def status_display(self, obj):
        return obj.status

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration_minutes', 'level')
    search_fields = ('title', 'category')
    list_filter = ('category', 'level')
    list_display_links = ('title',)
    inlines = [EventInline]
    @admin.display(description='Duration')
    def duration_display(self, obj):
        return f"{obj.duration_minutes} min"
    @admin.display(description='Events')
    def events_count(self, obj):
        return obj.events.count()


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'speciality', 'experience', 'photo', 'active_clubs', 'upcoming_events')
    list_display_links = ('full_name',)
    list_filter = ('speciality',)
    search_fields = ('full_name', 'speciality', 'experience')
    readonly_fields = ('photo_preview_large',)
    raw_id_fields = ()
    inlines = [TrainerClubInline, EventInline]
    def photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="width: 100px; height: auto; border-radius: 5px;" />')
        return "No photo uploaded"
    photo.short_description = 'Current Photo'
    @admin.display(description='Current Photo')
    def photo_preview_large(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="width: 200px; height: auto; border-radius: 5px;" />')
        return "No photo uploaded"
    @admin.display(description='Active Clubs')
    def active_clubs(self, obj):
        return obj.trainer_clubs.filter(is_active=True).count()
    @admin.display(description='Upcoming Events')
    def upcoming_events(self, obj):
        from django.utils import timezone
        return obj.events.filter(start_at__gte=timezone.now(), status='scheduled').count()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'trainer_id', 'club_id', 'start_at', 'status', 'booked_count', 'is_upcoming', 'duration')
    list_display_links = ('class_id', 'trainer_id')
    list_filter = ('status', 'club_id', 'class_id', 'start_at')
    search_fields = ('class_id__title', 'trainer_id__full_name', 'club_id__name', 'description')
    date_hierarchy = 'start_at'
    raw_id_fields = ('class_id', 'trainer_id', 'club_id')
    readonly_fields = ('booked_count', 'duration')
    inlines = [BookingInline]
    @admin.display(description='Upcoming', boolean=True)
    def is_upcoming(self, obj):
        from django.utils import timezone
        return obj.start_at > timezone.now() and obj.status == 'scheduled'
    @admin.display(description='Duration')
    def duration(self, obj):
        if obj.start_at and obj.end_at:
            diff = obj.end_at - obj.start_at
            minutes = diff.total_seconds() / 60
            return f"{int(minutes)} min"
        return "N/A"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'event_info', 'status_display', 'created_at')
    list_display_links = ('user_id', 'event_info')
    list_filter = ('status', 'created_at', 'event_id__class_id')
    search_fields = ('user_id__username', 'event_id__class_id__title', 'event_id__trainer_id__full_name')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user_id', 'event_id')
    readonly_fields = ('created_at', 'status_display')
    @admin.display(description='Event')
    def event_info(self, obj):
        return f"{obj.event_id.class_id.title} with {obj.event_id.trainer_id.full_name}"
    @admin.display(description='Status', boolean=True)
    def status_display(self, obj):
        return obj.status


@admin.register(Trainer_club)
class Trainer_clubAdmin(admin.ModelAdmin):
    list_display = ('trainer_id', 'club_id', 'is_active', 'created_at')
    list_display_links = ('trainer_id', 'club_id')
    list_filter = ('is_active', 'created_at', 'club_id')
    search_fields = ('trainer_id__full_name', 'club_id__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)