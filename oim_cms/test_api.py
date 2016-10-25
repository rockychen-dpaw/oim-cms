from django.contrib.auth.models import User
from django.test import TestCase, Client
import json
from mixer.backend.django import mixer
import random
import string
from uuid import uuid1

from organisation.models import DepartmentUser, Location, OrgUnit, CostCentre
from registers.models import ITSystem


def random_dpaw_email():
    """Return a random email address ending in dpaw.wa.gov.au
    """
    s = ''.join(random.choice(string.ascii_letters) for i in range(20))
    return '{}@dpaw.wa.gov.au'.format(s)


class ApiTestCase(TestCase):
    client = Client()

    def setUp(self):
        # Generate some other DepartmentUser objects.
        mixer.cycle(5).blend(
            DepartmentUser, photo=None, active=True,
            email=random_dpaw_email, org_unit=None,
            cost_centre=None)
        # Generate some locations.
        self.loc1 = mixer.blend(Location, manager=None)
        self.loc2 = mixer.blend(Location, manager=None)
        # Generate a basic org structure.
        # NOTE: don't use mixer to create OrgUnit objects (it breaks MPTT).
        self.dept = OrgUnit.objects.create(name='Department 1', unit_type=0)
        self.div1 = OrgUnit.objects.create(
            name='Divison 1', unit_type=1, parent=self.dept, location=self.loc1)
        self.cc1 = CostCentre.objects.create(
            name='Cost centre 1', code='001', division=self.div1, org_position=self.div1)
        self.div2 = OrgUnit.objects.create(
            name='Divison 2', unit_type=1, parent=self.dept, location=self.loc2)
        self.cc2 = CostCentre.objects.create(
            name='Cost centre 2', code='002', division=self.div2, org_position=self.div2)
        # Give each of the divisions some members.
        users = DepartmentUser.objects.all()
        self.user1 = users[0]
        self.user1.org_unit = self.div1
        self.user1.cost_centre = self.cc1
        self.user1.save()
        self.div1.manager = self.user1
        self.div1.save()
        self.user2 = users[1]
        self.user2.org_unit = self.div2
        self.user2.cost_centre = self.cc2
        self.user2.save()
        self.div2.manager = self.user2
        self.div2.save()
        # Mark a user as inactive and deleted in AD.
        self.del_user = users[2]
        self.del_user.active = False
        self.del_user.ad_deleted = True
        self.del_user.org_unit = self.div2
        self.del_user.cost_centre = self.cc2
        self.del_user.save()
        # Make a contractor.
        self.contract_user = users[3]
        self.contract_user.contractor = True
        self.contract_user.org_unit = self.div2
        self.contract_user.cost_centre = self.cc2
        self.contract_user.save()
        # Make a shared account.
        self.shared = users[4]
        self.shared.account_type = 5  # Shared account type.
        self.shared.org_unit = self.div1
        self.shared.cost_centre = self.cc1
        self.shared.save()
        # Generate some IT Systems.
        self.it1 = mixer.blend(ITSystem, status=0, owner=self.user1)
        self.it2 = mixer.blend(ITSystem, status=1, owner=self.user2)
        # Generate a test user for endpoint responses.
        self.testuser = User.objects.create_user(
            username='testuser', email='user@dpaw.wa.gov.au.com', password='pass')
        # Create a DepartmentUser object for testuser.
        mixer.blend(
            DepartmentUser, photo=None, active=True, email=self.testuser.email,
            org_unit=None, cost_centre=None)
        # Log in testuser by default.
        self.client.login(username='testuser', password='pass')


class ProfileTestCase(ApiTestCase):
    url = '/api/profile/'

    def test_profile_api_get(self):
        """Test the profile API endpoint GET response
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_profile_api_post(self):
        """Test the profile API endpoint GET response
        """
        response = self.client.get(self.url)
        j = json.loads(response.content)
        obj = j['objects'][0]
        self.assertFalse(obj['telephone'])
        tel = '9111 1111'
        response = self.client.post(self.url, {'telephone': tel})
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        obj = j['objects'][0]
        self.assertEqual(obj['telephone'], tel)

    def test_profile_api_anon(self):
        """Test that anonymous users can't use the profile endpoint
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class OptionResourceTestCase(ApiTestCase):

    def test_data_org_structure(self):
        """Test the data_org_structure API endpoint
        """
        url = '/api/options?list=org_structure'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Division 1 will be present in the response.
        self.assertContains(response, self.div1.name)
        # Response can be deserialised into a dict.
        r = json.loads(response.content)
        self.assertTrue(isinstance(r, dict))
        # Deserialised response contains a list.
        self.assertTrue(isinstance(r['objects'], list))
        # Remove all members from an org unit to test exclusion.
        self.user1.org_unit = None
        self.user1.cost_centre = None
        self.user1.save()
        self.shared.org_unit = None
        self.shared.cost_centre = None
        self.shared.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Division 1 won't be present in the response.
        self.assertNotContains(response, self.div1.name)

    def test_data_cost_centre(self):
        """Test the data_cost_centre API endpoint
        """
        url = '/api/options?list=cost_centre'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # 001 will be present in the response.
        self.assertContains(response, self.cc1.code)
        # Add 'inactive' to Division 1 name to inactivate the CC.
        self.div1.name = 'Division 1 (inactive)'
        self.div1.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # 001 won't be present in the response.
        self.assertNotContains(response, self.cc1.code)

    def test_data_org_unit(self):
        """Test the data_org_unit API endpoint
        """
        url = '/api/options?list=org_unit'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Org unit names will be present in the response.
        self.assertContains(response, self.dept.name)
        self.assertContains(response, self.div1.name)
        self.assertContains(response, self.div2.name)

    def test_data_dept_user(self):
        """Test the data_dept_user API endpoint
        """
        url = '/api/options?list=dept_user'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # User 1 will be present in the response.
        self.assertContains(response, self.user1.email)
        # Make a user inactive to test excludion
        self.user1.active = False
        self.user1.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # User 1 won't be present in the response.
        self.assertNotContains(response, self.user1.email)


class DepartmentUserResourceTestCase(ApiTestCase):

    def test_user_list(self):
        """Test the DepartmentUserResource list responses
        """
        url = '/api/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content)
        self.assertTrue(isinstance(r['objects'], list))
        # Response should not contain inactive, contractors or shared accounts.
        self.assertContains(response, self.user1.email)
        self.assertNotContains(response, self.del_user.email)
        self.assertNotContains(response, self.contract_user.email)
        self.assertNotContains(response, self.shared.email)
        # Test the compact response.
        url = '/api/users/?compact=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Test the minimal response.
        url = '/api/users/?minimal=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_list_filtering(self):
        """Test the DepartmentUserResource filtered list responses
        """
        # Test the "all" response.
        url = '/api/users/?all=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contract_user.email)
        self.assertContains(response, self.del_user.email)
        self.assertContains(response, self.shared.email)
        # Test filtering by ad_deleted.
        url = '/api/users/?ad_deleted=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.del_user.email)
        self.assertNotContains(response, self.user1.email)
        url = '/api/users/?ad_deleted=false'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.del_user.email)
        self.assertContains(response, self.user1.email)
        # Test filtering by email (should return only one object).
        url = '/api/users/?email={}'.format(self.user1.email)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j['objects']), 1)
        self.assertContains(response, self.user1.email)
        self.assertNotContains(response, self.user2.email)
        # Test filtering by GUID (should return only one object).
        url = '/api/users/?ad_guid={}'.format(self.user1.ad_guid)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j['objects']), 1)
        self.assertContains(response, self.user1.email)
        self.assertNotContains(response, self.user2.email)
        # Test filtering by cost centre (should return all, inc. inactive and contractors).
        url = '/api/users/?cost_centre={}'.format(self.cc2.code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.email)
        self.assertContains(response, self.contract_user.email)
        self.assertContains(response, self.del_user.email)
        self.assertNotContains(response, self.user1.email)
        self.assertNotContains(response, self.shared.email)  # Belongs to CC1.

    def test_org_structure(self):
        """Test the DepartmentUserResource org_structure response
        """
        url = '/api/users/?org_structure=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # User 1 will be present in the response.
        self.assertContains(response, self.user1.email)
        # Test sync_o365=true request parameter.
        self.div1.sync_o365 = False
        self.div1.save()
        url = '/api/users/?org_structure=true&sync_o365=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Division 1 won't be present in the response.
        self.assertNotContains(response, self.div1.name)
        # Test populate_groups=true request parameter.
        self.user1.populate_primary_group = False
        self.user1.save()
        url = '/api/users/?org_structure=true&populate_groups=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # User 1 won't be present in the response.
        self.assertNotContains(response, self.user1.email)

    def test_create(self):
        """Test the DepartmentUserResource create response
        """
        url = '/api/users/'
        # Response should be status 400 where ObjectGUID is missing.
        data = {}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # Try again with valid data.
        data = {
            'ObjectGUID': str(uuid1()),
            'EmailAddress': 'testemail@dpaw.wa.gov.au',
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Created
        # A DepartmentUser with that email should now exist.
        self.assertTrue(DepartmentUser.objects.filter(email='testemail@dpaw.wa.gov.au').exists())

    def test_update(self):
        """Test the DepartmentUserResource update response
        """
        url = '/api/users/'
        data = {
            'EmailAddress': self.user1.email,
            'GivenName': 'John',
            'Surname': 'Doe',
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete(self):
        """Test the DepartmentUserResource update response (set user as 'AD deleted')
        """
        self.assertFalse(self.user1.ad_deleted)
        self.assertTrue(self.user1.active)
        url = '/api/users/'
        data = {
            'EmailAddress': self.user1.email,
            'Deleted': 'true',
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        user = DepartmentUser.objects.get(pk=self.user1.pk)  # Refresh from db
        self.assertTrue(user.ad_deleted)
        self.assertFalse(user.active)


class LocationResourceTestCase(ApiTestCase):

    def test_list(self):
        """Test the LocationResource list response
        """
        url = '/api/locations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Test filtering by location_id.
        url = '/api/locations/?location_id={}'.format(self.loc1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ITSystemResourceTestCase(ApiTestCase):

    def test_list(self):
        """Test the ITSystemResource list response
        """
        url = '/api/itsystems/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # The 'development' IT system won't be in the response.
        self.assertNotContains(response, self.it2.name)
        # Test all request parameter.
        url = '/api/itsystems/?all'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # The 'development' IT system will be in the response.
        self.assertContains(response, self.it2.name)
        # Test filtering by system_id
        url = '/api/itsystems/?system_id={}'.format(self.it1.system_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.it1.name)
        self.assertNotContains(response, self.it2.name)
