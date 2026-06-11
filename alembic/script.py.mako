#!/usr/bin/env python
"""Script for Alembic autogenerate templates."""
from alembic import op
import sqlalchemy as sa

% if imports:
${imports}
% endif

def upgrade():
% for stmt in upgrade_ops:
    ${stmt}
% endfor

def downgrade():
% for stmt in downgrade_ops:
    ${stmt}
% endfor
"""A generic script template for Alembic autogenerate.
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    pass

def downgrade():
    pass
