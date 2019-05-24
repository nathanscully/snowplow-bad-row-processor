
import download
import process
import click
import sys

@click.command()
@click.option('--bucket')
@click.option('--filter')
@click.option('--error')
@click.option('--no-dl', default=False, is_flag=True)
def main(bucket, filter, error, no_dl):
    if not no_dl:
        dl = download.Downloader(bucket, filter)
        dl.run()

    process.Processor(error).run()

if __name__ == '__main__':
    sys.exit(main())
