#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from oslo.utils import timeutils

from heat.engine import notification
from heat.tests import common
from heat.tests import utils


class StackTest(common.HeatTestCase):

    def setUp(self):
        super(StackTest, self).setUp()
        self.ctx = utils.dummy_context()

    def test_send(self):
        created_time = timeutils.utcnow()
        st = mock.Mock()
        st.state = ('x', 'f')
        st.status = st.state[0]
        st.action = st.state[1]
        st.name = 'fred'
        st.status_reason = 'this is why'
        st.created_time = created_time
        st.context = self.ctx
        st.identifier.return_value.arn.return_value = 'hay-are-en'

        notify = self.patchobject(notification, 'notify')

        notification.stack.send(st)
        notify.assert_called_once_with(
            self.ctx, 'stack.f.error', 'ERROR',
            {'state_reason': 'this is why',
             'user_id': 'test_username',
             'stack_identity': 'hay-are-en',
             'stack_name': 'fred',
             'tenant_id': 'test_tenant_id',
             'create_at': timeutils.isotime(created_time),
             'state': 'x_f'})


class AutoScaleTest(common.HeatTestCase):
    def setUp(self):
        super(AutoScaleTest, self).setUp()
        self.ctx = utils.dummy_context()

    def test_send(self):
        created_time = timeutils.utcnow()
        st = mock.Mock()
        st.state = ('x', 'f')
        st.status = st.state[0]
        st.action = st.state[1]
        st.name = 'fred'
        st.status_reason = 'this is why'
        st.created_time = created_time
        st.context = self.ctx
        st.identifier.return_value.arn.return_value = 'hay-are-en'

        notify = self.patchobject(notification, 'notify')

        notification.autoscaling.send(st, adjustment='x',
                                      adjustment_type='y',
                                      capacity='5',
                                      groupname='c',
                                      message='fred',
                                      suffix='the-end')
        notify.assert_called_once_with(
            self.ctx, 'autoscaling.the-end', 'INFO',
            {'state_reason': 'this is why',
             'user_id': 'test_username',
             'stack_identity': 'hay-are-en',
             'stack_name': 'fred',
             'tenant_id': 'test_tenant_id',
             'create_at': timeutils.isotime(created_time),
             'state': 'x_f', 'adjustment_type': 'y',
             'groupname': 'c', 'capacity': '5',
             'message': 'fred', 'adjustment': 'x'})

    def test_send_error(self):
        created_time = timeutils.utcnow()
        st = mock.Mock()
        st.state = ('x', 'f')
        st.status = st.state[0]
        st.action = st.state[1]
        st.name = 'fred'
        st.status_reason = 'this is why'
        st.created_time = created_time
        st.context = self.ctx
        st.identifier.return_value.arn.return_value = 'hay-are-en'

        notify = self.patchobject(notification, 'notify')

        notification.autoscaling.send(st, adjustment='x',
                                      adjustment_type='y',
                                      capacity='5',
                                      groupname='c',
                                      suffix='error')
        notify.assert_called_once_with(
            self.ctx, 'autoscaling.error', 'ERROR',
            {'state_reason': 'this is why',
             'user_id': 'test_username',
             'stack_identity': 'hay-are-en',
             'stack_name': 'fred',
             'tenant_id': 'test_tenant_id',
             'create_at': timeutils.isotime(created_time),
             'state': 'x_f', 'adjustment_type': 'y',
             'groupname': 'c', 'capacity': '5',
             'message': 'error', 'adjustment': 'x'})
