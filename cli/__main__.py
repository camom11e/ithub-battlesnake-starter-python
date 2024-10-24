import run

process = run.main(browser=True)()

while text := process.stdout.decode("utf-8"):
    print(text, end="", flush=True)
