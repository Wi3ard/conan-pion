#include <pion/http/parser.hpp>
#include <pion/http/request.hpp>

int main()
{
	try
	{
		pion::http::parser parser(true);
		pion::http::request request;
	}
	catch (const std::exception&)
	{
	}

	return 0;
}
