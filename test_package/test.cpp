#include <pion/http/parser.hpp>
#include <pion/http/request.hpp>

int main()
{
	try
	{
		pion::http::parser parser(true);
	}
	catch (const std::exception& e)
	{
		std::cerr << e.what() << std::endl;
	}

	return 0;
}
