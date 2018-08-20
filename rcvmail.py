# -*- coding: utf-8 -*-
import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import re

def rcvmail(email, passwd, pop3_server):
	# email = input("Email: ")
	# passwd = input("Passwd: ")
	# pop3_server = input('POP3 Server: ')
	server = poplib.POP3(pop3_server)

	# print(server.getwelcome)
	server.user(email)
	server.pass_(passwd)

	# print('Messages: %s. Size: %s' % server.stat())

	resp, mails, octets = server.list()

	# print(mails)

	index = len(mails)

	resp, lines, octets = server.retr(index)
	lines = [elem.decode('utf-8') for elem in lines]
	msg_content = '\n'.join(lines)
	msg = Parser().parsestr(msg_content)

	server.quit()

	return msg

def print_info(msg, indent = 0):
	if indent==0:
		for header in ['From','To','Subject']:
			value = msg.get(header,'')
			if value:
				if header=='Subject':
					value = decode_str(value)
				else:
					hdr, addr = parseaddr(value)
					name = decode_str(hdr)
					value = u'%s <%s>' % (name, addr)
			print('%s%s: %s' % ('  ' * indent, header, value))
	if (msg.is_multipart()):
		parts = msg.get_payload()
		for n, part in enumerate(parts):
			print('%spart %s' % ('  ' * indent, n))
			print('%s------------------' % ('  ' * indent))
			print_info(part, indent + 1)
	else:
		content_type = msg.get_content_type()
		if content_type == 'text/plain' or content_type == 'text/html':
			content = msg.get_payload(decode=True)
			charset = guess_charset(msg)
			print(charset)
			if charset:
				content = content.decode(charset)
			# print('%sText: %s' % ('  ' * indent, content + '...'))
			print(get_verify_code(content))

		else:
			print('%sAttachment: %s' % ('  ' * indent, content_type))

def getMailText(msg):
	src = msg.get('From','')
	hdr, addr = parseaddr(src)
	name = decode_str(hdr)

	if name == 'baidu':
		content_type = msg.get_content_type()
		if content_type == 'text/plain' or content_type == 'text/html':
			content = msg.get_payload(decode=True)
			charset = guess_charset(msg)
			if charset:
				content = content.decode(charset)
			# print('%sText: %s' % ('  ' * indent, content + '...'))
			return get_verify_code(content)
		else:
			return None
	else:
		return None



def get_verify_code(msg):
	result = re.search(r'.*>(\d{6})</b>.*', msg)
	if result:
		return result.group(1)
	else:
		return None

def decode_str(s):
	value, charset = decode_header(s)[0]
	if charset:
		value = value.decode(charset)
	return value

def guess_charset(msg):
	charset = msg.get_charset()
	if charset is None:
		content_type = msg.get('Content-Type','').lower()
		pos = content_type.find('charset=')
		if pos >= 0:
			charset = content_type[pos+8:].strip()
	return charset

# if __name__ == '__main__':
# 	msg = rcvmail('hpky92@163.com','a43906','pop.163.com')
# 	print(getMailText(msg))




