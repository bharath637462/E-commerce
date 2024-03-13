from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utills.models import ModelMixin, BaseModelMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Role(ModelMixin):
    name = models.CharField(verbose_name=_('Name'), max_length=50, unique=True, help_text=_('User role name'))
    description = models.TextField(verbose_name=_('Description'), blank=True, help_text=_('User role description'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name',)


class UserManager(BaseUserManager):
    """
    Inherits BaseUserManager class
    """

    def create_user(self, email, password=None, **other_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        if not password:
            password = self.model.objects.make_random_password(length=14,
                                                               allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

        user = self.model(email=self.normalize_email(email), **other_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        if not password:
            password = self.model.objects.make_random_password(length=14,
                                                               allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.role = Role.objects.filter(name='Admin').first()
        user.save(using=self._db)
        return user


class User(BaseModelMixin, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('email'), max_length=200, unique=True, help_text=_('Primary email'))
    first_name = models.CharField(verbose_name=_('First Name'), max_length=255, help_text=_('First name'))
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=255, blank=True, help_text=_('Last name'))
    phone = PhoneNumberField(verbose_name=_('Phone'), help_text=_('Phone Number'))
    role = models.ForeignKey(Role, verbose_name=_('Role'), related_name='users',
                             default='ce80048d-7158-425b-8713-9e9c335aaea0', null=True, on_delete=models.SET_NULL,
                             help_text=_('Role'))
    is_staff = models.BooleanField(verbose_name=_('Is staff user?'), default=False)
    is_superuser = models.BooleanField(verbose_name=_('Is superuser?'), default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return '{0}[{1}]'.format(self.full_name, self.email)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()
        super(User, self).save(*args, **kwargs)

    @property
    def full_name(self):
        if self.last_name:
            return f"{self.first_name.strip().title()} {self.last_name.strip().title()}"

        return self.first_name.strip().title()

    class Meta:
        db_table = 'user'
        verbose_name = _('Users')
        verbose_name_plural = _('Users')


class AddressType(ModelMixin):
    name = models.CharField(_('Name'), max_length=255, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'address_type'
        verbose_name = _('Address Type')
        verbose_name_plural = _('Address Types')


class Country(ModelMixin):
    name = models.CharField(verbose_name=_('Name'), max_length=100, unique=True, help_text=_('Country name'))
    calling_code = models.CharField(verbose_name=_('Calling code'), max_length=10, help_text=_('Telephone calling code (Example: +1 for United States)'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'country'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ('name',)


class State(ModelMixin):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states', help_text=_('Country'))
    name = models.CharField(verbose_name=_('Name'), max_length=100, help_text=_('State name'))

    def __str__(self):
        return self.name.title()

    class Meta:
        db_table = 'state'
        unique_together = ('country', 'name')
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ('name',)


class Address(ModelMixin):
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='addresses', on_delete=models.CASCADE,
                             help_text=_('User'))
    type = models.ForeignKey(AddressType, verbose_name=_('Type'), default='b9325b51-3d1d-46fb-99a6-39634de5e3c0',
                             related_name='addresses', null=True, on_delete=models.SET_NULL, help_text=_('Type'))
    address_line1 = models.CharField(verbose_name=_('Address Line 1'), max_length=255, help_text=_('Address line 1'))
    address_line2 = models.CharField(verbose_name=_('Address Line 2'), max_length=255, blank=True,
                                     help_text=_('Address line 2'))
    city = models.CharField(verbose_name=_('City'), max_length=100, blank=True, help_text=_('City'))
    state = models.ForeignKey(State, verbose_name=_('State'), related_name='addresses', null=True,
                              on_delete=models.SET_NULL, help_text=_('State'))
    country = models.ForeignKey(Country, verbose_name=_('Country'), related_name='addresses', null=True,
                                on_delete=models.SET_NULL, help_text=_('Country'))
    postal_code = models.CharField(verbose_name=_('Postal Code'), max_length=15, help_text=_('Postal code'))
    phone = PhoneNumberField(verbose_name=_('Phone'), blank=True, help_text=_('Phone Number'))
    landmark = models.CharField(verbose_name=_('Landmark'), max_length=255, blank=True, help_text=_('Landmark'))

    def __str__(self):
        return self.user.first_name

    class Meta:
        db_table = 'address'
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


class Color(ModelMixin):
    name = models.CharField(_('Name'), max_length=255, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'color'
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')


class Category(ModelMixin):
    name = models.CharField(_('Name'), max_length=255, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class SubCategory(ModelMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories', help_text=_('Category'))
    name = models.CharField(_('Name'), max_length=255, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subCategory'
        verbose_name = _('SubCategory')
        unique_together = ('category', 'name')
        verbose_name_plural = _('SubCategories')

class Test(ModelMixin):
    name = models.CharField(_('Name'), max_length=255, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Test'
        verbose_name = _('Test')
        verbose_name_plural = _('Test')


class Product(ModelMixin):
    sub_category = models.ForeignKey(SubCategory, verbose_name=_('Sub Category'), related_name='products',
                                     on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    image = models.ImageField(upload_to='static/img')
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    tests = models.ManyToManyField(Test, verbose_name=_('Test'), blank=True, related_name='products',
                                    )
    colors = models.ManyToManyField(Color, verbose_name=_('Color'), blank=True, related_name='products', through='ProductColors')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class TransactionType(ModelMixin):
    name = models.CharField(_('Name'), max_length=255, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'transaction_type'
        verbose_name = _('Transaction Type')
        verbose_name_plural = _('Transaction Types')


class Order(ModelMixin):
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='orders',
                             on_delete=models.SET_NULL, blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name=_('Products'), related_name='orders', through='OrderProducts')
    transaction_type = models.OneToOneField(TransactionType, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='orders')

    @property
    def total(self):
        return sum(product.price for product in self.products.all())

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'order'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class Rating(ModelMixin):
    choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    rating = models.SmallIntegerField(_('Rating'), choices=choices, null=True, blank=True, help_text=_('How likely are'
                                                                                                       ' you to recommend'))
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='ratings',
                             on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='ratings',
                                on_delete=models.SET_NULL, blank=True, null=True)
    comments = models.TextField(verbose_name=_('Comments'), blank=True, null=True)

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = 'rating'
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')


class Cart(ModelMixin):
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='carts',
                             on_delete=models.SET_NULL, blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name=_('Products'), related_name='carts', through='CartProducts')

    def __str__(self):
        return self.user.first_name

    class Meta:
        db_table = 'cart'
        verbose_name = _('Cart')
        verbose_name_plural = _('Cart')


class ProductColors(BaseModelMixin):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='product_colors',
                             on_delete=models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey(Color, verbose_name=_('Color'), related_name='product_colors',
                                on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = 'product_colors'
        verbose_name = _('Product Colors')
        verbose_name_plural = _('Product Colors')


class CartProducts(BaseModelMixin):
    products = models.ForeignKey(Product, verbose_name=_('product'), related_name='cart_products',
                             on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(Cart, verbose_name=_('Cart'), related_name='cart_products',
                                on_delete=models.SET_NULL, blank=True, null=True)
    product_colors = models.ForeignKey(ProductColors, verbose_name=_('Product Colors'), related_name='cart_products',
                                       on_delete=models.SET_NULL, blank=True, null=True)
    count = models.IntegerField(verbose_name=_('Count'), default=1)

    def __str__(self):
        return self.products.name

    class Meta:
        db_table = 'cart_products'
        verbose_name = _('Cart Products')
        verbose_name_plural = _('Cart Products')


class OrderProducts(BaseModelMixin):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='order_products',
                             on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, verbose_name=_('Order'), related_name='order_products',
                                on_delete=models.SET_NULL, blank=True, null=True)
    product_colors = models.ForeignKey(ProductColors, verbose_name=_('Product Colors'), related_name='order_products',
                                on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = 'order_products'
        verbose_name = _('Order Products')
        verbose_name_plural = _('Order Products')
