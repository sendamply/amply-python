"""Amply /api/v1/email request builder"""

from .email_address import EmailAddress

class EmailHelper(object):
    """Parse email data"""

    def __init__(self):
        """Parse email data"""

        self.request_data = {}

    def parsed_data(self, data):
        """Build the request object"""

        self.set_from(data.get('from'))
        self.set_subject(data.get('subject'))
        self.set_text(data.get('text'))
        self.set_html(data.get('html'))
        self.set_content(data.get('content'))
        self.set_reply_to(data.get('reply_to'))
        self.set_template(data.get('template'))
        self.set_dynamic_template_data(data.get('dynamic_template_data'))
        self.set_unsubscribe_group_uuid(data.get('unsubscribe_group_uuid'))
        self.set_ip_or_pool_uuid(data.get('ip_or_pool_uuid'))
        self.set_attachments(data.get('attachments'))
        self.set_headers(data.get('headers'))
        self.set_categories(data.get('categories'))
        self.set_clicktracking(data.get('clicktracking'))
        self.set_substitutions(data.get('substitutions'))

        personalizations = data.get('personalizations')
        if personalizations is not None:
            self.set_personalizations(personalizations)
        else:
            self.set_personalizations_from_to(
                data.get('to'),
                data.get('cc'),
                data.get('bcc')
            )

        return self.request_data

    def set_from(self, from_address):
        """Set the from of your email"""

        if from_address is None:
            return

        self.request_data['from'] = self.format_emails(from_address)[0]

    def set_subject(self, subject):
        """Set the subject of your email"""

        if not isinstance(subject, str):
            raise Exception('String expected for `subject`')

        self.request_data['subject'] = subject

    def set_text(self, text):
        """Set the text part of the email"""

        if text is None:
            return

        self.request_data['content'] = self.request_data.get('content') or []
        self.request_data['content'].append({'type': 'text/plain', 'value': text})


    def set_html(self, html):
        """Set the html part of your email"""

        if html is None:
            return

        self.request_data['content'] = self.request_data.get('content') or []
        self.request_data['content'].append({'type': 'text/html', 'value': html})

    def set_content(self, content):
        """Set custom content types"""

        if content is None:
            return

        if not isinstance(content, list):
            raise Exception('Array expected for `content`')

        self.request_data['content'] = self.request_data.get('content') or []

        length = len(content)

        for i in range(length):
            if not isinstance(content[i], dict):
                raise Exception("Invalid `content[%i]`" %(i))

            if content[i].get('type') is None:
                raise Exception("`type` must be defined for `content[%i]`" %(i))

            if content[i].get('value') is None:
                raise Exception("`value` must be defined for `content[%i]`" %(i))

            self.request_data['content'].append({'type': content[i]['type'], 'value': content[i]['value']})

    def set_reply_to(self, reply_to):
        """Set the Reply-To"""

        if reply_to is None:
            return

        self.request_data['reply_to'] = self.format_emails(reply_to)[0]

    def set_template(self, template):
        """Set the `template`
        Create templates at https://sendamply.com/home/templates
        """
        if template is None:
            return

        self.request_data['template'] = template

    def set_dynamic_template_data(self, dynamic_template_data):
        """Set dynamic template variables"""

        if dynamic_template_data is None:
            return

        if not isinstance(dynamic_template_data, dict):
            raise Exception('Dictionary expected for `dynamic_template_data`')

        self.request_data['substitutions'] = self.request_data.get('substitutions') or {}

        for var in dynamic_template_data:
            self.request_data['substitutions'][var] = str(dynamic_template_data[var])

    def set_unsubscribe_group_uuid(self, unsubscribe_group_uuid):
        """Set the unsubscribe group"""

        if unsubscribe_group_uuid is None:
            return

        self.request_data['unsubscribe_group_uuid'] = unsubscribe_group_uuid

    def set_ip_or_pool_uuid(self, ip_or_pool_uuid):
        """Set the IP address or IP pool you want to send from
        Default is Global
        """
        if ip_or_pool_uuid is None:
            return

        self.request_data['ip_or_pool_uuid'] = ip_or_pool_uuid

    def set_attachments(self, attachments):
        """Set attachments"""

        if attachments is None:
            return

        if not isinstance(attachments, list):
            raise Exception('List expected for `attachments`')

        parsed_attachments = []
        length = len(attachments)

        for i in range(length):
            if not isinstance(attachments[i], dict):
                raise Exception("Invalid `attachments[%i]`" %(i))

            try:
                valid_content_types = (str, unicode)
            except NameError:
                valid_content_types = str

            if not isinstance(attachments[i].get('content'), valid_content_types):
                raise Exception("`attachments[%i][content]` is required" %(i))

            if not isinstance(attachments[i].get('filename'), str):
                raise Exception("`attachments[%i][filename]` is required" %(i))

            parsed_attachments.append({
                'content': attachments[i]['content'],
                'filename': attachments[i]['filename'],
                'type': attachments[i].get('type'),
                'disposition': attachments[i].get('disposition')
            })

        self.request_data['attachments'] = parsed_attachments

    def set_headers(self, headers):
        """Set headers you want to send with your email"""

        if headers is None:
            return

        if not isinstance(headers, dict):
            raise Exception('Dictionary expected for `headers`')

        self.request_data['headers'] = self.request_data.get('headers') or {}

        for key in headers:
            self.request_data['headers'][key] = str(headers[key])

    def set_categories(self, categories):
        """Set categories to tag your email with
        Analytics will show up at
        https://sendamply.com/home/analytics/email_categories
        """
        if categories is None:
            return

        if not isinstance(categories, list):
            raise Exception('List expected for `categories`')

        self.request_data['analytics'] = self.request_data.get('analytics') or {}
        self.request_data['analytics']['categories'] = []

        for category in categories:
            self.request_data['analytics']['categories'].append(str(category))

    def set_clicktracking(self, clicktracking):
        """Enable/disable clicktracking
        This takes priority over your default setting from
        https://sendamply.com/home/settings/general
        """
        if clicktracking is None:
            return

        self.request_data['analytics'] = self.request_data.get('analytics') or {}
        self.request_data['analytics']['clicktracking'] = not not clicktracking

    def set_substitutions(self, substitutions):
        """Create substitutions"""

        if substitutions is None:
            return

        if not isinstance(substitutions, dict):
            raise Exception('Dictionary expected for `substitutions`')

        self.request_data['substitutions'] = self.request_data.get('substitutions') or {}

        for key in substitutions:
            self.request_data['substitutions'][key] = str(substitutions[key])

    def set_personalizations(self, personalizations):
        """Full control over the recipients of your email
        This takes priority over setting to, cc, and bcc
        """

        self.request_data['personalizations'] = personalizations

    def set_personalizations_from_to(self, to, cc, bcc):
        """Set the to, cc, and bcc of your email"""

        self.request_data['personalizations'] = [{}]

        if to is None and cc is None and bcc is None:
            raise Exception('Provide at least one of `to`, `cc` or `bcc`')

        if to is not None:
            self.request_data['personalizations'][0]['to'] = self.format_emails(to)

        if cc is not None:
            self.request_data['personalizations'][0]['cc'] = self.format_emails(cc)

        if bcc is not None:
            self.request_data['personalizations'][0]['bcc'] = self.format_emails(bcc)

    @staticmethod
    def format_emails(emails):
        """Format emails to send to Amply API"""

        if isinstance(emails, list):
            return [EmailAddress(email).to_json() for email in emails]

        return [EmailAddress(emails).to_json()]
