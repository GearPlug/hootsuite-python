import requests
from urllib.parse import urlencode
from hootsuite import exceptions


class Client(object):
    BASE = 'https://apis.hootsuite.com/'

    def __init__(self, api_key, secret):
        self.client_id = api_key
        self.client_secret = secret
        self.base_url = self.BASE + '/'
        self.token = None

    def authorization_url(self, redirect_uri, scope):
        """
        Args:
            redirect_uri: The redirect_uri of your app, where authentication responses can be sent and received by
            your app.  It must exactly match one of the redirect_uris you registered in the app registration portal
            scope: .
        Returns:
            A string.
        """
        endpoint = 'auth/oauth/v2/authorize'
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': ' '.join(scope),
            'response_type': 'code',
        }
        return self.BASE + endpoint + urlencode(params)

    def exchange_code(self, redirect_uri, code):
        """Exchanges a code for a Token.
        Args:
            redirect_uri: The redirect_uri of your app, where authentication responses can be sent and received by
            your app.  It must exactly match one of the redirect_uris you registered in the app registration portal
            code: The authorization_code that you acquired in the first leg of the flow.
        Returns:
            A dict.
        """
        endpoint = 'auth/oauth/v2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
        }
        response = requests.post(self.BASE + endpoint, params=data)
        return self._parse(response)

    def refresh_token(self, redirect_uri, refresh_token):
        """
        Args:
            redirect_uri: The redirect_uri of your app, where authentication responses can be sent and received by
            your app.  It must exactly match one of the redirect_uris you registered in the app registration portal
            refresh_token: An OAuth 2.0 refresh token. Your app can use this token acquire additional access tokens
            after the current access token expires. Refresh tokens are long-lived, and can be used to retain access
            to resources for extended periods of time.
        Returns:
            A dict.
        """
        endpoint = 'auth/oauth/v2/token'
        data = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }
        response = requests.post(self.BASE + endpoint, params=data)
        return self._parse(response)

    def set_token(self, token):
        """Sets the Token for its use in this library.
        Args:
            token: A string with the Token.
        """
        self.token = token

    def send_echo(self):
        """
        Test connection with Hootsuite
        :return:
        """
        endpoint = 'v1/echo'
        data = {
            "message": "Test connection"
        }
        return self._post(endpoint, data)

    # User
    def get_account_info(self):
        """
        Return basic information about account
        Returns:

        """
        endpoint = 'account'
        return self._get(endpoint)

    def get_me(self):
        """
        Get user authenticated user info
        :return:
        """
        endpoint = 'v1/me'
        return self._get(endpoint)

    def get_my_organization(self):
        """
        Get user authenticated user organization info
        :return:
        """
        endpoint = 'v1/me/organizations'
        return self._get(endpoint)

    def get_my_social_profiles(self):
        """
        Get user authenticated user social profiles
        :return:
        """
        endpoint = 'v1/me/socialProfiles'
        return self._get(endpoint)

    def get_member(self, member_id):
        """
        Get member by id
        :return:
        """
        endpoint = 'v1/members/{0}'.format(member_id)
        return self._get(endpoint)

    def create_member(self, email, full_name, org_name, bio, timezone):
        """
        Create new member in a HootSuite org.
        Requires organization manage members permission.
        :return:
        """
        data = {
            "organizationIds": [
                "626731"
            ],
            "email": "{0}".format(email),  # Example jsmith@test.com
            "fullName": "{0}".format(full_name),  # Example Joe Smith
            "companyName": "{0}".format(org_name),  # Example Hootsuite
            "bio": "{0}".format(bio),  # Example short/middle bio
            "timezone": "{0}".format(timezone),  # Example America/Vancouver
            "language": "en"
        }
        endpoint = 'v1/members'
        return self._post(endpoint, data=data)

    def get_members_organizations(self, member_id):
        """
        Get the organizations a member is in
        :param member_id:
        :return:
        """
        endpoint = 'v1/members/{0}/organizations'.format(member_id)
        return self._get(endpoint)

    # Messages
    def create_schedule_messages(
            self, text, social_profile_ids, scheduled_send_time, webhook_urls, fb_age_min, fb_age_max, fb_edu,
            fb_gender, fb_interested_in, fb_relationship_status, fb_country, fb_regions, fb_cities, fb_locales,
            fb_visibility, lkin_company_size, lkin_geography, lkin_industry, lkin_jobfuction, lkin_seniority,
            lkin_visibility, gplus_visibility, email_notification, tags
    ):
        """
        TODO: location, media, mediaUrls
        :param text:
        :param social_profile_ids: list of profiles ids
        :param scheduled_send_time: 2020-01-01T14:00:00Z
        :param webhook_urls: list of urls
        :param fb_age_min:
        :param fb_age_max:
        :param fb_edu: ["collegeGrad"]
        :param fb_gender: ["male"]
        :param fb_interested_in: ["female"]
        :param fb_relationship_status: ["single"]
        :param fb_country: {"country": Canada, "code": "CA"}
        :param fb_regions: {"region": "British Columbia", "key": The region key, as provided by Facebook.}
        :param fb_cities: {"cities": "Burnaby, BC", "key": The city key, as provided by Facebook.}
        :param fb_locales: {"locales": "Burnaby, BC", "key": The locale key, as provided by Facebook.}
        :param fb_visibility:  "everyone" "friends" "friendsOfFriends"
        :param lkin_company_size: Company size to target the message at.
        :param lkin_geography: Geography to target the message at
        :param lkin_industry: Industry to target the message at
        :param lkin_jobfuction: Job function to target the message at.
        :param lkin_seniority: Senority to target the message at
        :param lkin_visibility: "anyone" "connectionsOnly"
        :param gplus_visibility: "public" "myCircles" "extendedCircles"
        :param email_notification: true or false
        :param tags: list of tags
        :return:
        """
        endpoint = 'v1/messages'
        data = {
            "text": "".format(text),
            "socialProfileIds": "{0}".format(social_profile_ids),
            "scheduledSendTime": "{0}".format(scheduled_send_time),
            "webhookUrls": "{0}".format(webhook_urls),
            "tags": "{0}".format(tags),
            "targeting": {
                "facebookPage": {
                    "ageMin": fb_age_min,
                    "ageMax": fb_age_max,
                    "education": "{0}".format(fb_edu),
                    "genders": "{0}".format(fb_gender),
                    "interestedIn": "{0}".format(fb_interested_in),
                    "relationshipStatus": "{0}".format(fb_relationship_status),
                    "countries": [
                        {
                            "k": "{}".format(fb_country['countrys']),
                            "v": "{}".format(fb_country['code'])
                        }
                    ],
                    "regions": [
                        {
                            "k": "{}".format(fb_regions['regions']),
                            "v": "{}".format(fb_regions['key'])
                        }
                    ],
                    "cities": [
                        {
                            "k": "{}".format(fb_cities['cities']),
                            "v": "{}".format(fb_regions['key'])
                        }
                    ],
                    "locales": [
                        {
                            "k": "{}".format(fb_locales['locales']),
                            "v": "{}".format(fb_regions['key'])
                        },
                    ]},
                "linkedInCompany":
                    {
                        "companySize": ["{}".format(lkin_company_size)],
                        "geography": ["{}".format(lkin_geography)],
                        "industry": ["{}".format(lkin_industry)],
                        "jobFunction": ["{}".format(lkin_jobfuction)],
                        "seniority": ["{}".format(lkin_seniority)],
                    }
                },
            "privacy": {
                "facebook": {
                    "visibility": ["{0}".format(fb_visibility)]
                },
                "googlePlus": {
                    "visibility": ["{0}".format(gplus_visibility)]
                },
                "linkedIn": {
                    "visibility": ["{0}".format(lkin_visibility)]
                }
            },
            "location": {
                "latitude": 57.64911,
                "longitude": 10.40744
            },
            "emailNotification": email_notification,
            "mediaUrls": [
                {
                    "url": ""
                }
            ],
            "media": [
                {
                    "id": "",
                    "videoOptions": {
                        "facebook": {
                            "title": "",
                            "category": ""
                        }
                    }
                }
            ]
        }
        endpoint = 'v1/messages'
        return self._post(endpoint, data=data)

    def get_outbound_messsages(self, starttime, endtime, state=None, social_profiles_ids=None, limit=None):
        """

        :param starttime: The start date range of messages to be returned. In ISO-8601 format.
        :param endtime: The end date range of messages to be returned. In ISO-8601 format.
                        Must not be later than 4 weeks from startTime.
        :param state:   A filter to return messages with in the matching state.
                        Allowed values are PENDING_APPROVAL, REJECTED, SENT, SCHEDULED and SEND_FAILED_PERMANENTLY.
        :param social_profiles_ids: A filter to return messages for certain social profiles. Integer
        :param limit: Maximum number of messages to be returned in the response. Defaults to 50 if not specified.
                      Maximum allowable limit is 100. Integer
        :return:
        """
        endpoint = 'v1/messages'
        params = {
            'startTime': '{}'.format(starttime),
            'endTime': '{}'.format(endtime),
            'state': '{}'.format(state, ''),
            'socialProfileIds': '{}'.format(social_profiles_ids, ''),
            'limit': '{}'.format(limit, '')
        }
        return self._get(endpoint, params=params)

    def get_message(self, message_id):
        """
        :param message_id: id of message
        :return:
        """
        endpoint = 'v1/messages/{0}'.format(message_id)
        return self._get(endpoint)

    def delete_message(self, message_id):
        """
        :param message_id: id of message to delete
        :return:
        """
        endpoint = 'v1/messages/{0}'.format(message_id)
        return self._delete(endpoint)

    def aprove_message(self, message_id, sequence_number, reviewer_type):
        """
        :param message_id: id of message to aprove
        :param sequence_number: The sequence number of the message being approved.
        :param reviewer_type: "EXTERNAL" "MEMBER"
        :return:
        """
        endpoint = 'v1/messages/{0}/approve'.format(message_id)
        data = {
            "sequenceNumber": sequence_number,
            "reviewerType": "{0}".format(reviewer_type)
        }
        return self._post(endpoint, data=data)

    def reject_message(self, message_id, sequence_number, reviewer_type, reason):
        """

        :param message_id: id of message to aprove
        :param sequence_number: The sequence number of the message being approved.
        :param reviewer_type: "EXTERNAL" "MEMBER"
        :param reason: The rejection reason to be displayed to the creator of the message.
        :return:
        """
        endpoint = 'v1/messages/{0}/reject'.format(message_id)
        data = {
            "sequenceNumber": sequence_number,
            "reviewerType": "{0}".format(reviewer_type),
            "reason": "{0}".format(reason)
        }
        return self._post(endpoint, data=data)

    # Organization
    def get_organization_members(self, organization_id):
        """
        :param organization_id: id of organization
        :return:
        """
        endpoint = 'v1/organizations/{0}/members'.format(organization_id)
        return self._get(endpoint)

    def remove_member_from_organization(self, organization_id, member_id):
        """

        :param organization_id: id of organization
        :param member_id: id of member to remove from organization
        :return:
        """
        endpoint = 'v1/organizations/{0}/members/{1}'.format(organization_id, member_id)
        return self._delete(endpoint)

    # Requests area
    def _get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def _patch(self, endpoint, **kwargs):
        return self._request('PATCH', endpoint, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        _headers = {
            'X-PW-AccessToken': "{}".format(self.api_key),
            'X-PW-Application': "developer_api",
            'X-PW-UserEmail': "{}".format(self.email),
            'Content-Type': "application/json"
        }
        url = self.base_url + endpoint
        return self._parse(requests.request(method, url, headers=_headers, **kwargs))

    def _parse(self, response):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        if status_code in (200, 201, 202):
            return r
        elif status_code == 204:
            return None
        elif status_code == 400:
            raise exceptions.BadRequest(r)
        elif status_code == 401:
            raise exceptions.Unauthorized(r)
        elif status_code == 403:
            raise exceptions.Forbidden(r)
        elif status_code == 404:
            raise exceptions.NotFound(r)
        elif status_code == 405:
            raise exceptions.MethodNotAllowed(r)
        elif status_code == 406:
            raise exceptions.NotAcceptable(r)
        elif status_code == 409:
            raise exceptions.Conflict(r)
        elif status_code == 410:
            raise exceptions.Gone(r)
        elif status_code == 411:
            raise exceptions.LengthRequired(r)
        elif status_code == 412:
            raise exceptions.PreconditionFailed(r)
        elif status_code == 413:
            raise exceptions.RequestEntityTooLarge(r)
        elif status_code == 415:
            raise exceptions.UnsupportedMediaType(r)
        elif status_code == 416:
            raise exceptions.RequestedRangeNotSatisfiable(r)
        elif status_code == 422:
            raise exceptions.UnprocessableEntity(r)
        elif status_code == 429:
            raise exceptions.TooManyRequests(r)
        elif status_code == 500:
            raise exceptions.InternalServerError(r)
        elif status_code == 501:
            raise exceptions.NotImplemented(r)
        elif status_code == 503:
            raise exceptions.ServiceUnavailable(r)
        elif status_code == 504:
            raise exceptions.GatewayTimeout(r)
        elif status_code == 507:
            raise exceptions.InsufficientStorage(r)
        elif status_code == 509:
            raise exceptions.BandwidthLimitExceeded(r)
        else:
            raise exceptions.UnknownError(r)