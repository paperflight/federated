# Lint as: python3
# Copyright 2018, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from absl.testing import absltest

from tensorflow_federated.python.core.impl import context_base
from tensorflow_federated.python.core.impl import context_stack_test_utils
from tensorflow_federated.python.core.impl.context_stack import context_stack_impl


class ContextStackTest(absltest.TestCase):

  def test_set_default_context_with_none(self):
    context = context_stack_test_utils.TestContext('test')
    context_stack = context_stack_impl.ContextStackImpl()
    context_stack.set_default_context(context)
    self.assertIs(context_stack.current, context)

    context_stack.set_default_context(None)

    self.assertIsNot(context_stack.current, context)
    self.assertIsInstance(context_stack.current, context_base.Context)

  def test_set_default_context_with_context(self):
    context = context_stack_test_utils.TestContext('test')
    context_stack = context_stack_impl.ContextStackImpl()
    self.assertIsNot(context_stack.current, context)

    context_stack.set_default_context(context)

    self.assertIs(context_stack.current, context)

  def test_install_pushes_context_on_stack(self):
    context_stack = context_stack_impl.ContextStackImpl()
    self.assertIsInstance(context_stack.current, context_base.Context)

    context_one = context_stack_test_utils.TestContext('test')
    with context_stack.install(context_one):
      self.assertIs(context_stack.current, context_one)

      context_two = context_stack_test_utils.TestContext('test')
      with context_stack.install(context_two):
        self.assertIs(context_stack.current, context_two)

      self.assertIs(context_stack.current, context_one)

    self.assertIsInstance(context_stack.current, context_base.Context)


if __name__ == '__main__':
  absltest.main()
