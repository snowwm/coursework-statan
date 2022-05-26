// !test uninit_var

int main(void)
{
	int i = 0;
	int err;
	string s1 = func("test", 123), s2, s3 = "test";
	mytype a1 = func("test", 123, i), a2 = "test";
	
	cout << i << err << s1 << s2 << s3;

	return 0;
}
