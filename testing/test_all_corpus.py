from unittest import defaultTestLoader, TextTestRunner


def discover_and_run(start_dir: str = 'C:\\Users\\Lenovo\\PycharmProjects\\ScientificArticles\\testing\\sentence_testing', pattern: str = 'test*.py'):
    """Discover and run tests cases, returning the result."""
    tests = defaultTestLoader.discover(start_dir, pattern=pattern)
    runner = TextTestRunner()
    result = runner.run(tests)
    print(result.errors, result.failures)
    return result


if __name__ == '__main__':
    discover_and_run()
