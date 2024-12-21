from django.db import models

from django.utils.translation import gettext_lazy as _

# from django.db import models

from django.contrib.auth.models import (

    BaseUserManager, AbstractBaseUser

)

from django.contrib.auth.models import (

        Group,

    Permission

)

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):

        """

        Creates and saves a User with the given email and password.

        """

        if not email:

            raise ValueError('Users must have an email address')

        user = self.model(

            email=self.normalize_email(email),

        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_staffuser(self, email, password):

        """

        Creates and saves a staff user with the given email and password.

        """

        user = self.create_user(

            email,

            password=password,

        )

        user.is_staff = True

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        """

        Creates and saves a superuser with the given email and password.

        """

        user = self.create_user(

            email,

            password=password,

        )

        user.is_staff = True

        user.is_superuser = True

        user.save(using=self._db)

        return user
    



# Role Model
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class User(AbstractBaseUser):

    username = models.CharField(

        verbose_name="Username",

        max_length=255,

        default="",

        blank=True, 

        unique=False,

    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True, help_text="User is verified and have access to the website. Admin can also block a user by un-check this field")
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False, help_text="Superuser of the whole website.") 
    roles = models.ManyToManyField(Role, related_name="users", blank=True)
    groups = models.ManyToManyField(

        Group,

        verbose_name=_('groups'),

        blank=True,

        help_text=_(

            'The groups this user belongs to. A user will get all permissions '

            'granted to each of their groups.'

        ),

        related_name="user_groups_set",

        related_query_name="user",

    )

    permissions = models.ManyToManyField(

        Permission,

        verbose_name=_('user permissions'),

        blank=True,

        help_text=_('Specific permissions for this user.'),

        related_name="user_permissions_set",

        related_query_name="user",

    )

    date_joined = models.DateTimeField(_('Date Joined'), blank=True, null=True, auto_now_add=True) 

    updated= models.DateTimeField( verbose_name= _('Last Updated Timestamp') , auto_now= True)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [] # Email & Password are required by default.

    

    def get_full_name(self):

        # The user is identified by their email address

        return self.email

    def get_short_name(self):

        # The user is identified by their email address

        return self.email

    def __str__(self):

        return self.email

    def has_perm(self, perm, obj=None):

        "Does the user have a specific permission?"

        # Simplest possible answer: Yes, always

        return True

    def has_module_perms(self, app_label):

        "Does the user have permissions to view the app `app_label`?"

        # Simplest possible answer: Yes, always

        return True

    objects = UserManager()

    # @property

    # def is_staff(self):

    #     "Is the user a member of staff?"

    #     return self.is_staff

    # @property

    # def is_superuser(self):

    #     "Is the user a admin member?"

    #     return self.is_superuser
