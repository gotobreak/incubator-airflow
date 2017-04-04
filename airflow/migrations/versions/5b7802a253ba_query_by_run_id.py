#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""query_by_run_id

Revision ID: 5b7802a253ba
Revises: 127d2bf2dfa7
Create Date: 2017-03-10 05:54:23.625241

"""

# revision identifiers, used by Alembic.
revision = '5b7802a253ba'
down_revision = '127d2bf2dfa7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('task_instance', sa.Column('run_id', sa.String(length=250), nullable=True))
#    op.execute('UPDATE task_instance SET task_instance.run_id=(SELECT dag_run.run_id FROM dag_run WHERE dag_run.dag_id=task_instance.dag_id)')
#    op.create_unique_constraint("ti_unique_di_ti_ri", "task_instance", ["dag_id", "task_id", "run_id"])
    op.create_index('ti_state_run_id', 'task_instance', ['dag_id', 'task_id', 'run_id', 'state'], unique=False)
    op.create_index('ti_state_main', 'task_instance', ['dag_id', 'task_id', 'run_id', 'execution_date', 'state'], unique=False)

    op.add_column('task_fail', sa.Column('run_id', sa.String(length=250), nullable=True))
#    op.create_unique_constraint("tf_unique_di_ti_ri", "task_fail", ["dag_id", "task_id", "run_id"])


def downgrade():
    op.drop_column('run_id', 'task_instance')
    op.drop_constraint('ti_unique_di_ti_ri', 'task_instance')
    op.drop_index('ti_state_run_id', table_name='task_instance')
    op.drop_index('ti_state_main', table_name='task_instance')

    op.drop_column('run_id', 'task_fail')
    op.drop_constraint('tf_unique_di_ti_ri', 'tf_unique_di_ti_ri')
