std::vector<unsigned char> getPi() {
	std::vector<unsigned char> arr;

	std::ifstream input("data.pi");
	if (!input.is_open()) {
		std::cout << "Wrong input file name!" << std::endl;
		return arr;
	}
	std::streambuf *cinbuf = std::cin.rdbuf();
	std::cin.rdbuf(input.rdbuf());

	unsigned char chr = 0;
	while (!std::cin.eof()) {
		chr = std::cin.get();
		if (chr == '0' || chr == '1')
			arr.push_back(chr);
	}

	std::cin.rdbuf(cinbuf);
	return arr;
}

std::vector<unsigned char> getSequance() {
	std::vector<unsigned char> arr;

	std::ifstream input("sequence.txt");
	if (!input.is_open()) {
		std::cout << "Wrong input file name!" << std::endl;
		return arr;
	}
	std::streambuf *cinbuf = std::cin.rdbuf();
	std::cin.rdbuf(input.rdbuf());

	unsigned char chr = 0;
	while (!std::cin.eof()) {
		chr = std::cin.get();
		if (chr == '0' || chr == '1')
			arr.push_back(chr);
	}

	std::cin.rdbuf(cinbuf);
	return arr;
}
