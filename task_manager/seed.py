"""Seed the database with realistic test data for a general organization."""
from datetime import datetime, timedelta
import random
from app import create_app
from models import db
from models.user import User
from models.team import Team
from models.task import Task, Tag
from models.comment import Comment
from models.notification import Notification

app = create_app()

USERS = [
    {'username': 'admin', 'email': 'admin@company.org', 'full_name': 'Admin User', 'role': 'admin', 'job_title': 'Platform Administrator', 'department': 'Administration', 'bio': 'System administrator for the task management platform.'},
    {'username': 'maria.ionescu', 'email': 'maria.i@company.org', 'full_name': 'Maria Ionescu', 'role': 'manager', 'job_title': 'Operations Director', 'department': 'Operations', 'bio': 'Overseeing daily operations and process improvement across all departments.'},
    {'username': 'andrei.popa', 'email': 'andrei.p@company.org', 'full_name': 'Andrei Popa', 'role': 'manager', 'job_title': 'Marketing Manager', 'department': 'Marketing', 'bio': 'Leading brand strategy, campaigns, and client outreach initiatives.'},
    {'username': 'elena.radu', 'email': 'elena.r@company.org', 'full_name': 'Elena Radu', 'role': 'user', 'job_title': 'Senior Accountant', 'department': 'Finance', 'bio': 'Financial reporting, budgeting, and compliance.'},
    {'username': 'cristian.mihai', 'email': 'cristian.m@company.org', 'full_name': 'Cristian Mihai', 'role': 'user', 'job_title': 'Sales Representative', 'department': 'Sales', 'bio': 'Managing client relationships and driving revenue growth.'},
    {'username': 'ana.vasile', 'email': 'ana.v@company.org', 'full_name': 'Ana Vasile', 'role': 'user', 'job_title': 'HR Specialist', 'department': 'Human Resources', 'bio': 'Recruitment, onboarding, and employee development programs.'},
    {'username': 'bogdan.stan', 'email': 'bogdan.s@company.org', 'full_name': 'Bogdan Stan', 'role': 'user', 'job_title': 'Logistics Coordinator', 'department': 'Operations', 'bio': 'Supply chain management and distribution coordination.'},
    {'username': 'diana.florea', 'email': 'diana.f@company.org', 'full_name': 'Diana Florea', 'role': 'user', 'job_title': 'Graphic Designer', 'department': 'Marketing', 'bio': 'Visual branding, print materials, and digital content creation.'},
    {'username': 'george.tudor', 'email': 'george.t@company.org', 'full_name': 'George Tudor', 'role': 'manager', 'job_title': 'Finance Director', 'department': 'Finance', 'bio': 'Strategic financial planning and budget oversight.'},
    {'username': 'ioana.barbu', 'email': 'ioana.b@company.org', 'full_name': 'Ioana Barbu', 'role': 'user', 'job_title': 'Executive Assistant', 'department': 'Administration', 'bio': 'Scheduling, correspondence, and office management support.'},
    {'username': 'radu.marin', 'email': 'radu.m@company.org', 'full_name': 'Radu Marin', 'role': 'user', 'job_title': 'Customer Support Lead', 'department': 'Sales', 'bio': 'Customer satisfaction, complaint resolution, and support team coordination.'},
    {'username': 'laura.neagu', 'email': 'laura.n@company.org', 'full_name': 'Laura Neagu', 'role': 'user', 'job_title': 'Legal Advisor', 'department': 'Legal', 'bio': 'Contract review, regulatory compliance, and corporate governance.'},
]

TEAMS = [
    {'name': 'Operations', 'description': 'Day-to-day business operations, process optimization, logistics, and facility management.', 'color': '#2563eb'},
    {'name': 'Marketing & Communications', 'description': 'Brand management, advertising campaigns, social media, and public relations.', 'color': '#ec4899'},
    {'name': 'Finance & Accounting', 'description': 'Budgeting, financial reporting, invoicing, payroll, and regulatory compliance.', 'color': '#10b981'},
    {'name': 'Human Resources', 'description': 'Recruitment, onboarding, training, employee relations, and performance reviews.', 'color': '#f97316'},
    {'name': 'Sales & Client Relations', 'description': 'Client acquisition, account management, sales pipeline, and customer support.', 'color': '#8b5cf6'},
    {'name': 'Administration & Legal', 'description': 'Office management, contracts, legal compliance, and executive support.', 'color': '#64748b'},
]

TEAM_MEMBERS = {
    'Operations': ('maria.ionescu', ['bogdan.stan']),
    'Marketing & Communications': ('andrei.popa', ['diana.florea']),
    'Finance & Accounting': ('george.tudor', ['elena.radu']),
    'Human Resources': ('maria.ionescu', ['ana.vasile']),
    'Sales & Client Relations': ('andrei.popa', ['cristian.mihai', 'radu.marin']),
    'Administration & Legal': ('admin', ['ioana.barbu', 'laura.neagu']),
}

TAGS = ['urgent', 'budget', 'client', 'internal', 'compliance', 'training', 'report', 'meeting', 'deadline', 'approval', 'vendor', 'hiring', 'event', 'policy', 'review']

TASKS = [
    {'title': 'Prepare Q1 budget report for board meeting', 'description': 'Compile all departmental expenses, revenue figures, and variance analysis for the Q1 board presentation. Include year-over-year comparisons and projections for Q2.', 'priority': 'high', 'status': 'in_progress', 'team': 'Finance & Accounting', 'creator': 'george.tudor', 'assignee': 'elena.radu', 'tags': ['report', 'budget', 'deadline'], 'days_ago': 5, 'deadline_days': 3},
    {'title': 'Organize new employee onboarding for March cohort', 'description': 'Prepare onboarding materials, schedule orientation sessions, set up workstations and accounts for 4 new hires starting March 15th.', 'priority': 'high', 'status': 'todo', 'team': 'Human Resources', 'creator': 'maria.ionescu', 'assignee': 'ana.vasile', 'tags': ['hiring', 'training'], 'days_ago': 3, 'deadline_days': 8},
    {'title': 'Redesign company brochure for trade show', 'description': 'Update the company brochure with new product lines, recent client testimonials, and refreshed branding. Need 500 printed copies by March 20th.', 'priority': 'high', 'status': 'review', 'team': 'Marketing & Communications', 'creator': 'andrei.popa', 'assignee': 'diana.florea', 'tags': ['event', 'deadline'], 'days_ago': 10, 'deadline_days': 5},
    {'title': 'Negotiate warehouse lease renewal', 'description': 'Current warehouse lease expires April 30th. Research market rates, prepare negotiation points, and schedule meeting with the landlord. Target: 5% reduction or improved terms.', 'priority': 'critical', 'status': 'in_progress', 'team': 'Operations', 'creator': 'maria.ionescu', 'assignee': 'bogdan.stan', 'tags': ['vendor', 'deadline', 'budget'], 'days_ago': 7, 'deadline_days': 14},
    {'title': 'Update employee handbook with new remote work policy', 'description': 'Draft the updated remote work policy based on management decisions. Include eligibility criteria, equipment provisions, communication expectations, and performance metrics.', 'priority': 'medium', 'status': 'in_progress', 'team': 'Human Resources', 'creator': 'maria.ionescu', 'assignee': 'ana.vasile', 'tags': ['policy', 'internal'], 'days_ago': 4, 'deadline_days': 10},
    {'title': 'Follow up with Meridian Corp on proposal', 'description': 'Sent proposal last week for the annual service contract. Call the procurement contact, address any concerns, and push for decision by end of month.', 'priority': 'high', 'status': 'todo', 'team': 'Sales & Client Relations', 'creator': 'andrei.popa', 'assignee': 'cristian.mihai', 'tags': ['client', 'deadline'], 'days_ago': 3, 'deadline_days': 5},
    {'title': 'Process monthly vendor invoices', 'description': 'Review and process all pending vendor invoices for February. Verify amounts against purchase orders, code to correct accounts, and submit for approval.', 'priority': 'medium', 'status': 'todo', 'team': 'Finance & Accounting', 'creator': 'george.tudor', 'assignee': 'elena.radu', 'tags': ['vendor', 'budget', 'deadline'], 'days_ago': 1, 'deadline_days': 3},
    {'title': 'Plan company summer team-building event', 'description': 'Research venues, activities, and catering options for the annual team-building event (80+ attendees). Prepare 3 proposals with different budget tiers for management review.', 'priority': 'low', 'status': 'todo', 'team': 'Administration & Legal', 'creator': 'admin', 'assignee': 'ioana.barbu', 'tags': ['event', 'budget'], 'days_ago': 8, 'deadline_days': 30},
    {'title': 'Review and renew supplier contracts', 'description': 'Three supplier contracts expire next quarter. Review terms, compare with competing offers, and prepare renewal recommendations for each.', 'priority': 'critical', 'status': 'in_progress', 'team': 'Administration & Legal', 'creator': 'maria.ionescu', 'assignee': 'laura.neagu', 'tags': ['vendor', 'compliance', 'review'], 'days_ago': 6, 'deadline_days': 10},
    {'title': 'Launch social media campaign for new product line', 'description': 'Create and schedule content for a 4-week social media campaign. Platforms: LinkedIn, Facebook, Instagram. Include visuals, copy, and a paid ads budget of 2000 EUR.', 'priority': 'high', 'status': 'todo', 'team': 'Marketing & Communications', 'creator': 'andrei.popa', 'assignee': 'diana.florea', 'tags': ['budget', 'deadline'], 'days_ago': 2, 'deadline_days': 7},
    {'title': 'Conduct quarterly inventory audit', 'description': 'Physical inventory count across both warehouse locations. Compare against system records, identify discrepancies, and prepare variance report.', 'priority': 'high', 'status': 'todo', 'team': 'Operations', 'creator': 'maria.ionescu', 'assignee': 'bogdan.stan', 'tags': ['compliance', 'report'], 'days_ago': 2, 'deadline_days': 5},
    {'title': 'Set up customer satisfaction survey', 'description': 'Design and distribute a customer satisfaction survey to our top 50 accounts. Use online survey tool, include NPS question, analyze results and present findings.', 'priority': 'medium', 'status': 'todo', 'team': 'Sales & Client Relations', 'creator': 'andrei.popa', 'assignee': 'radu.marin', 'tags': ['client', 'report'], 'days_ago': 4, 'deadline_days': 14},
    {'title': 'Schedule annual performance reviews', 'description': 'Coordinate with all department managers to schedule performance review meetings for all employees. Distribute review templates and set deadlines for self-assessments.', 'priority': 'medium', 'status': 'todo', 'team': 'Human Resources', 'creator': 'maria.ionescu', 'assignee': 'ana.vasile', 'tags': ['review', 'internal', 'meeting'], 'days_ago': 1, 'deadline_days': 21},
    {'title': 'Prepare monthly sales report', 'description': 'Compile February sales figures by region, product line, and sales representative. Include pipeline forecast and comparison against targets.', 'priority': 'high', 'status': 'in_progress', 'team': 'Sales & Client Relations', 'creator': 'andrei.popa', 'assignee': 'cristian.mihai', 'tags': ['report', 'deadline'], 'days_ago': 2, 'deadline_days': 2},
    {'title': 'Resolve shipping delays with DHL contract', 'description': 'Multiple clients reported late deliveries last month. Investigate root cause with DHL account manager, negotiate SLA improvements or explore alternative carriers.', 'priority': 'critical', 'status': 'done', 'team': 'Operations', 'creator': 'bogdan.stan', 'assignee': 'bogdan.stan', 'tags': ['vendor', 'client', 'urgent'], 'days_ago': 12, 'deadline_days': -2},
    {'title': 'Submit annual tax filings', 'description': 'Prepare and submit corporate tax returns for the fiscal year. Coordinate with external auditor for final review before submission deadline.', 'priority': 'critical', 'status': 'done', 'team': 'Finance & Accounting', 'creator': 'george.tudor', 'assignee': 'elena.radu', 'tags': ['compliance', 'deadline'], 'days_ago': 20, 'deadline_days': -5},
    {'title': 'Implement new visitor management system', 'description': 'Replace the paper logbook with a digital visitor management system. Research solutions, get quotes, install and train reception staff.', 'priority': 'low', 'status': 'done', 'team': 'Administration & Legal', 'creator': 'admin', 'assignee': 'ioana.barbu', 'tags': ['internal'], 'days_ago': 25, 'deadline_days': -10},
    {'title': 'Complete GDPR compliance audit', 'description': 'Review all data processing activities, update privacy policies, verify consent mechanisms, and prepare compliance report for management.', 'priority': 'high', 'status': 'done', 'team': 'Administration & Legal', 'creator': 'maria.ionescu', 'assignee': 'laura.neagu', 'tags': ['compliance', 'policy', 'report'], 'days_ago': 18, 'deadline_days': -3},
    {'title': 'Develop training materials for new CRM system', 'description': 'Create user guides, quick-reference cards, and a short video tutorial for the new CRM system rolling out next month. Coordinate with IT for system access.', 'priority': 'medium', 'status': 'todo', 'team': 'Sales & Client Relations', 'creator': 'maria.ionescu', 'assignee': 'radu.marin', 'tags': ['training', 'internal'], 'days_ago': 3, 'deadline_days': 12},
    {'title': 'Organize management strategy retreat', 'description': 'Plan a 2-day offsite strategy retreat for senior management (12 people). Book venue, prepare agenda, coordinate travel and accommodation. Budget: 5000 EUR.', 'priority': 'medium', 'status': 'todo', 'team': 'Administration & Legal', 'creator': 'admin', 'assignee': 'ioana.barbu', 'tags': ['event', 'meeting', 'budget'], 'days_ago': 5, 'deadline_days': 18},
]

COMMENTS = [
    {'task_idx': 0, 'user': 'elena.radu', 'content': 'Revenue figures are finalized. Working on the variance analysis now. Should have a draft by Thursday.', 'days_ago': 3},
    {'task_idx': 0, 'user': 'george.tudor', 'content': 'Good. Please include a cash flow projection slide as well. @maria.ionescu will need the operations budget breakdown from your team.', 'days_ago': 2},
    {'task_idx': 0, 'user': 'maria.ionescu', 'content': 'I will send the operations breakdown by tomorrow morning. We came in 3% under budget this quarter.', 'days_ago': 1},
    {'task_idx': 2, 'user': 'diana.florea', 'content': 'First draft is uploaded to the shared drive. Used the new color palette and included the client testimonials from Meridian and Apex.', 'days_ago': 5},
    {'task_idx': 2, 'user': 'andrei.popa', 'content': 'Looks great overall! Two changes:\n1. Move the pricing table to page 3\n2. Replace the stock photo on the cover with our team photo from the last event', 'days_ago': 4},
    {'task_idx': 2, 'user': 'diana.florea', 'content': 'Done. Updated version is in the shared drive. @andrei.popa please review when you get a chance.', 'days_ago': 3},
    {'task_idx': 3, 'user': 'bogdan.stan', 'content': 'Market rates in the area have increased 8% but our current landlord is willing to negotiate. Meeting scheduled for next Tuesday.', 'days_ago': 4},
    {'task_idx': 3, 'user': 'maria.ionescu', 'content': 'Good research. Let us aim for a 3-year term with a fixed rate. @laura.neagu can you review the current lease terms and flag any issues before the meeting?', 'days_ago': 3},
    {'task_idx': 5, 'user': 'cristian.mihai', 'content': 'Called their procurement office. They are comparing us with one other vendor. Decision expected by Friday. They asked for a 5% volume discount.', 'days_ago': 2},
    {'task_idx': 5, 'user': 'andrei.popa', 'content': 'We can offer 3% on orders above 50K. Prepare a revised quote with tiered pricing. @george.tudor needs to approve any discount above 3%.', 'days_ago': 1},
    {'task_idx': 8, 'user': 'laura.neagu', 'content': 'Reviewed the first two contracts. The logistics supplier has a problematic auto-renewal clause. Recommending we renegotiate that term.', 'days_ago': 3},
    {'task_idx': 8, 'user': 'maria.ionescu', 'content': 'Agreed. Flag any clauses that limit our ability to switch suppliers. @bogdan.stan please pull together delivery performance data so we have leverage.', 'days_ago': 2},
    {'task_idx': 13, 'user': 'cristian.mihai', 'content': 'Southern region numbers are in. We hit 112% of target. Northern region is lagging at 78% — need to discuss strategy.', 'days_ago': 1},
    {'task_idx': 13, 'user': 'andrei.popa', 'content': 'Good work on the south. Let us schedule a call about the northern region. @radu.marin any feedback from the clients up there?', 'days_ago': 1},
    {'task_idx': 14, 'user': 'bogdan.stan', 'content': 'Root cause identified: DHL changed their routing hub for our region without notice. They have reverted and offered a credit on the next invoice.', 'days_ago': 8},
    {'task_idx': 14, 'user': 'maria.ionescu', 'content': 'Good resolution. Make sure we get that credit in writing. @elena.radu please track the credit against next month invoices.', 'days_ago': 6},
    {'task_idx': 17, 'user': 'laura.neagu', 'content': 'Audit complete. Found 3 minor gaps in consent forms for marketing emails. Updated forms are ready for review. Full report attached.', 'days_ago': 10},
]

now = datetime.utcnow()


def seed():
    with app.app_context():
        print('Dropping all tables...')
        db.drop_all()
        print('Creating all tables...')
        db.create_all()

        # Create tags
        print('Creating tags...')
        tag_objects = {}
        for tag_name in TAGS:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            tag_objects[tag_name] = tag
        db.session.flush()

        # Create users
        print('Creating users...')
        user_objects = {}
        for u in USERS:
            user = User(
                username=u['username'],
                email=u['email'],
                full_name=u['full_name'],
                role=u['role'],
                job_title=u['job_title'],
                department=u['department'],
                bio=u['bio'],
                created_at=now - timedelta(days=random.randint(60, 365)),
            )
            user.set_password('password123')
            db.session.add(user)
            user_objects[u['username']] = user
        db.session.flush()

        # Set admin password differently
        user_objects['admin'].set_password('admin123')

        # Create teams
        print('Creating teams...')
        team_objects = {}
        for t in TEAMS:
            team = Team(name=t['name'], description=t['description'], color=t['color'])
            db.session.add(team)
            team_objects[t['name']] = team
        db.session.flush()

        # Assign team leads and members
        print('Assigning team members...')
        for team_name, (lead_username, member_usernames) in TEAM_MEMBERS.items():
            team = team_objects[team_name]
            lead = user_objects[lead_username]
            team.lead_id = lead.id
            if lead not in team.members.all():
                team.members.append(lead)
            for username in member_usernames:
                member = user_objects[username]
                if member not in team.members.all():
                    team.members.append(member)
        db.session.flush()

        # Create tasks
        print('Creating tasks...')
        task_objects = []
        for t in TASKS:
            creator = user_objects[t['creator']]
            assignee = user_objects.get(t['assignee'])
            team = team_objects.get(t['team'])
            deadline = now + timedelta(days=t['deadline_days']) if t['deadline_days'] else None
            task = Task(
                title=t['title'],
                description=t['description'],
                priority=t['priority'],
                status=t['status'],
                creator_id=creator.id,
                assignee_id=assignee.id if assignee else None,
                team_id=team.id if team else None,
                deadline=deadline,
                created_at=now - timedelta(days=t['days_ago']),
                updated_at=now - timedelta(days=max(0, t['days_ago'] - 2)),
            )
            for tag_name in t.get('tags', []):
                if tag_name in tag_objects:
                    task.tags.append(tag_objects[tag_name])
            db.session.add(task)
            task_objects.append(task)
        db.session.flush()

        # Create comments
        print('Creating comments...')
        for c in COMMENTS:
            task = task_objects[c['task_idx']]
            user = user_objects[c['user']]
            comment = Comment(
                content=c['content'],
                task_id=task.id,
                user_id=user.id,
                created_at=now - timedelta(days=c['days_ago']),
            )
            db.session.add(comment)
        db.session.flush()

        # Create some notifications
        print('Creating notifications...')
        for username in ['elena.radu', 'cristian.mihai', 'bogdan.stan', 'ana.vasile', 'diana.florea']:
            user = user_objects[username]
            for i in range(random.randint(2, 5)):
                notif = Notification(
                    user_id=user.id,
                    type=random.choice(['assignment', 'comment', 'deadline']),
                    message=random.choice([
                        'maria.ionescu assigned you a new task',
                        'New comment on: Q1 budget report',
                        'Deadline approaching: Vendor invoices due Friday',
                        'andrei.popa mentioned you in a comment',
                        'george.tudor commented on: Monthly sales report',
                    ]),
                    link='/tasks/1',
                    read=random.choice([True, False]),
                    created_at=now - timedelta(hours=random.randint(1, 72)),
                )
                db.session.add(notif)

        db.session.commit()
        print()
        print('=== Seed Complete ===')
        print(f'  Users:    {len(USERS)}')
        print(f'  Teams:    {len(TEAMS)}')
        print(f'  Tasks:    {len(TASKS)}')
        print(f'  Comments: {len(COMMENTS)}')
        print(f'  Tags:     {len(TAGS)}')
        print()
        print('Login credentials (all users use "password123" except admin):')
        print('  admin / admin123  (Administrator)')
        for u in USERS[1:]:
            print(f'  {u["username"]} / password123  ({u["role"]}, {u["department"]})')


if __name__ == '__main__':
    seed()
