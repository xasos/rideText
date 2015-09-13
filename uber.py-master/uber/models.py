from .model_base import ModelField, Model, DictField, Field, BooleanField, NumberField, ListField, FloatField,\
    DateTimeField, StringField, EpochField


class GPSLocation(object):
    """
    used to report extended gps information  to Uber
    """

    def __init__(self, latitude, longitude, altitude=None, vertical_accuracy=None, horizontal_accuracy=None):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.vertical_accuracy = vertical_accuracy
        self.horizontal_accuracy = horizontal_accuracy


class UberVehicleType(object):
    """
    The "fixed" Uber car types. Provided for convenience.
    On occasion Uber will add new car types (kitty car, ice cream truck etc). You can see all car types by examining
    app_state.city.vehicle_views
    """
    BLACK_CAR = 1
    UBERX = 8
    SUV = 2
    TAXI = 69


class ClientStatus(object):
    LOOKING = 'Looking'  # user is looking around
    DISPATCHING = 'Dispatching'
    WAITING_FOR_PICKUP = 'WaitingForPickup'


class RequestNote(object):
    REQUEST_EXPIRED = 'RequestExpired'


class DriverStatus(object):
    ACCEPTED = 'Accepted'


class SystemMessage(Model):
    """
    system messages by Uber. These are HTML messages.
    """
    id = Field('id')
    etag = Field('eTag')
    display_properties = Field('displayProps')
    modules = Field('modules')


class SimpleLocation(Model):
    latitude = FloatField('latitude')
    longitude = FloatField('longitude')


class VehicleLocation(SimpleLocation):
    """
    represents a vehicle location at a given time
    """
    epoch = EpochField('epoch')
    course = Field('course', optional=True)


class Fare(Model):
    id = NumberField('id')
    speed_threshold_mps = NumberField('speedThresholdMps')
    base = StringField('base')
    per_minute = StringField('perMinute')
    per_distance_unit = StringField('perDistanceUnit')
    distance_unit = StringField('distanceUnit')
    type = StringField('type')
    minimum = StringField('minimum')
    cancellation = StringField('cancellation')


class Place(Model):
    """
    Place metadata
    """
    id = NumberField('id')

    # 'foursquare'
    type = StringField('type')

    # 'Gym at 353 king st'
    nickname = StringField('nickname')

    formatted_address = StringField('formatted_address')

    distance = FloatField('distance')
    latitude = FloatField('latitude')
    longitude = FloatField('longitude')

    # GMaps-style components
    address_components = Field('address_components')


class Image(Model):
    url = StringField('url')
    width = NumberField('width')
    height = NumberField('height')


class WebView(Model):
    id = Field('id')
    html = StringField('html')


class Surge(Model):
    """
    Everyone's favorite surge pricing.
    """
    fare_id = NumberField('fareId')
    multiplier = FloatField('multiplier')
    expiration_time = NumberField('expirationTime')
    base_fee = StringField('base')
    per_distance_unit = StringField('perDistanceUnit')
    distance_unit = StringField('distanceUnit')
    per_minute = StringField('perMinute')
    speed_threshold_mps = NumberField('speedThresholdMps')
    minimum_fee = StringField('minimum')
    cancellation_fee = StringField('cancellation')
    web_view = ModelField('webView', WebView)


class VehicleView(Model):
    id = NumberField('id')
    fare = ModelField('fare', Fare)
    map_images = ListField('mapImages', Image)
    mono_images = ListField('monoImages', Image)

    # "Black Car", "SUV", "UberX", "TAXI"
    description = StringField('description')

    pickup_eta_string = StringField('pickupEtaString')
    allow_fare_estimate = BooleanField('allowFareEstimate')
    max_fare_splits = NumberField('maxFareSplits')

    capacity = NumberField('capacity')
    fare_details_url = StringField('fareDetailsUrl', optional=True)
    surge = ModelField('surge', Surge, optional=True)

    # ui strings
    confirm_pickup_button_string = StringField('confirmPickupButtonString')
    set_pickup_location_string = StringField('setPickupLocationString')
    request_pickup_button_string = StringField('requestPickupButtonString')
    pickup_button_string = StringField('pickupButtonString')
    none_available_string = StringField('noneAvailableString')


class City(Model):
    name = StringField('cityName')
    currency_code = StringField('currencyCode')

    # all the vehicle types
    vehicle_views = DictField('vehicleViews', VehicleView, key=int)
    vehicle_views_order = Field('vehicleViewsOrder')
    default_vehicle_view_id = NumberField('defaultVehicleViewId')


class NearbyVehicles(Model):
    eta_string = StringField('etaString', optional=True)
    eta_string_short = StringField('etaStringShort', optional=True)
    min_eta = NumberField('minEta', optional=True)
    sorry_message = StringField('sorryMsg', optional=True)
    vehicle_paths = DictField('vehiclePaths', lambda x: [VehicleLocation(location) for location in x], optional=True)

    @property
    def is_available(self):
        return self.sorry_message is None


class PaymentProfile(Model):
    id = NumberField('id')
    billing_country_iso2 = StringField('billingCountryIso2', optional=True)
    card_type = StringField('cardType')
    card_number = StringField('cardNumber')
    account_name = StringField('accountName', optional=True)
    token_type = StringField('tokenType', optional=True)
    card_expiration = DateTimeField('cardExpiration')

    # personal/business(?)
    use_case = StringField('useCase')


class Experiment(Model):
    treatment_group_serial = Field('treatment_group_serial', optional=True)

    # 'untreated', 'experiment', 'control' or weird stuff like 'g20g20_button'
    treatment_group_name = Field('treatment_group_name')

    def __init__(self, name, data):
        super(Experiment, self).__init__(data)
        self._name = name

    @property
    def name(self):
        """
        experiment name - 'Minneapolis_Free_G10G10', 'new_user_splash_testing', 'first_experiment_magical_test51' etc
        """
        return self._name


class CreditBalance(Model):
    """
    Didn't have any credits :P
    """
    pass


class Driver(Model):
    """
    Details about the driver of the ride.
    """
    id = Field('id')

    # never saw this set to True.
    display_company = BooleanField('displayCompany')

    partner_company = StringField('partnerCompany')
    location = ModelField('location', SimpleLocation)
    rating = FloatField('rating')
    status = Field('status')
    phone = StringField('mobile')
    name = StringField('name')
    picture_url = StringField('pictureUrl')


class FeedbackType(Model):
    id = Field('id')
    type = Field('type')
    description = Field('description')


class VehicleType(Model):
    id = NumberField('id')
    capacity = NumberField('capacity')
    make = StringField('make')
    model = StringField('model')


class Vehicle(Model):
    uuid = Field('uuid')

    vehicle_type = ModelField('vehicleType', VehicleType)
    exterior_color = StringField('exteriorColor')
    interior_color = StringField('interiorColor')
    license_plate = StringField('licensePlate')

    license_plate_country_id = Field('licensePlateCountryId')
    license_plate_state = StringField('licensePlateState')
    vehicle_view_id = Field('vehicleViewId')
    year = NumberField('year')

    vehicle_path = ListField('vehiclePath', VehicleLocation)


class TripState(object):
    DISPATCHING = 0
    DRIVING_TO_PICKUP = 1
    IN_PROGRESS = 2


class Trip(Model):
    """
    Represents a trip in all of its states
    """
    # ride info
    driver = ModelField('driver', Driver, optional=True)
    vehicle = ModelField('vehicle', Vehicle, optional=True)
    is_zero_tolerance = BooleanField('isZeroTolerance', optional=True)
    feedback_types = ListField('feedbackTypes', FeedbackType, optional=True)
    eta = NumberField('eta', optional=True)
    eta_string = Field('etaString', optional=True)
    eta_string_short = Field('etaStringShort', optional=True)

    dispatch_percent = FloatField('dispatchPercent', optional=True)

    payment_profile_id = NumberField('paymentProfileId')
    use_credits = BooleanField('useCredits')

    # geolocated
    pickup_location = Field('pickupLocation')

    cancel_dialog = Field('cancelDialog')

    @property
    def state(self):
        """
        The 'state' of the trip (derived from the model data)
        """
        if self.dispatch_percent is not None:
            return TripState.DISPATCHING
        elif self.eta is not None:
            return TripState.DRIVING_TO_PICKUP
        else:
            return TripState.IN_PROGRESS


class Client(Model):
    id = NumberField('id')

    # Oops :P
    rating = FloatField('rating')

    has_american_mobile = BooleanField('hasAmericanMobile')
    credit_balances = ListField('creditBalances', CreditBalance)
    payment_profiles = ListField('paymentProfiles', PaymentProfile)
    fare_split_fee_string = Field('fareSplitFeeString')
    last_selected_payment_profile_id = NumberField('lastSelectedPaymentProfileId')
    mobile_digits = StringField('mobileDigits')
    is_admin = BooleanField('isAdmin')
    role = Field('role')
    referral_code = StringField('referralCode')
    email = StringField('email')
    picture_url = StringField('pictureUrl')
    referral_url = StringField('referralUrl')
    first_name = StringField('firstName')

    # "US"
    mobile_country_iso2 = StringField('mobileCountryIso2')

    mobile = StringField('mobile')
    last_name = StringField('lastName')
    mobile_country_id = NumberField('mobileCountryId')
    login_token = StringField('token')
    has_to_opt_in_sms_notifications = BooleanField('hasToOptInSmsNotifications')

    # phone country code (+1 for US)
    mobile_country_code = StringField('mobileCountryCode')

    promotion = Field('promotion')
    has_confirmed_mobile = BooleanField('hasConfirmedMobile')

    # a value from ClientStatus
    status = StringField('status', optional=True)

    # a value from RequestNote
    last_request_note = StringField('lastRequestNote', optional=True)

    last_request_msg = StringField('lastRequestMsg', optional=True)

    @property
    def active_experiments(self):
        return {k: Experiment(k, v) for k, v in self._data['activeExperiments'].items()}


class ApiResponse(Model):
    data = Field('data', optional=True)
    error = Field('error', optional=True)

    @property
    def valid(self):
        return self.error is None


class AppState(Model):
    city = ModelField('city', City)
    nearby_vehicles = DictField('nearbyVehicles', NearbyVehicles, key=int, optional=True)
    client = ModelField('client', Client)

    # available when we order a ride
    trip = ModelField('trip', Trip, optional=True)

    # This is present when performing ApiCommands (add/remove payments), and is usually the raw data from the external
    # service (Braintree, PayPal etc) with a bit of Uber stuff on top.
    # So essentially, a lot of times the data will appear similar, but be different (camelCase vs underscore, more
    # fields etc).
    # Therefor, I've decided to just keep it as is.
    # The Uber client itself most likely never parses this part other than the error segment
    api_response = ModelField('apiResponse', ApiResponse, optional=True)
