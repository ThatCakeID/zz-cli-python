import argparse
import requests
import tabulate
import vlc


from readchar import readkey, key


endpoints = {
  'firestore': 'https://firestore.googleapis.com/v1'
}
firestore = {
  'project': 'zrytezene-thatcakeid',
  'database': '(default)'
}


def construct_final_endpoint(endpoint, project, db):
  return f"{endpoint}/projects/{project}/databases/{db}"


def list(params: dict = { 'pageSize': 512 }, prefix: str = None):
  global endpoints, firestore

  # Send a GET request to Firestore service endpoints
  request_url = construct_final_endpoint(endpoints['firestore'], firestore['project'], firestore['database'])
  request = requests.get(f"{request_url}/documents/musics", params=params)

  # check: status code (must be 200 OK)
  if request.status_code != requests.codes.ok:
    print("zryte-cli: error: Failed to retrieve music list")
    return

  # Create row arrays for "ID" and "Title" columns
  rows_id = []
  rows_title = []

  # Populate the row arrays with the needed values
  #
  # If the prefix parameter is not empty, only the songs
  # that start with it are only appended to the rows
  for document in request.json()['documents']:
    document_id = document['name'].split('/')[-1]
    document_title = document['fields']['title']['stringValue']

    if prefix is not None:
      if not document_title.lower().startswith(prefix):
        continue
    
    rows_id.append(document_id)
    rows_title.append(document_title)

  # Combine both columns into a single dictionary for tabulate to output
  table = {
    'ID': rows_id,
    'Title': rows_title
  }

  # Print the tabulated dictionary containing both ID and Title columns
  if len(rows_title) > 0:
    print(tabulate.tabulate(table, headers="keys"))
  else:
    print("zryte-cli: The list returned empty")


def stream(id):
  global endpoints, firestore

  # Send a GET request to Firestore service endpoints
  request_url = construct_final_endpoint(endpoints['firestore'], firestore['project'], firestore['database'])
  request = requests.get(f"{request_url}/documents/musics/{id}")

  # check: status code (must be 200 OK)
  if request.status_code != requests.codes.ok:
    print("zryte-cli: error: Could not get music information")
    return
  
  # Output various music information
  # Also give a hint to user for stopping the playback
  fields = request.json()['fields']
  field_title = fields['title']['stringValue']
  field_url = fields['music_url']['stringValue']
  print("zryte-cli: Tip: Press ESCAPE to stop playback")
  print(f"zryte-cli: Now streaming music: {field_title}")

  # Initialize VLC instance and play the music URL
  player = vlc.MediaPlayer(field_url)
  player.play()
  
  # Wait until the player's state is stopped
  #
  # While waiting, we can listen for certain keystrokes
  # for controlling the playback, quite useful right?
  while player.get_state() != vlc.State.Stopped:
    try:
      keystroke = readkey().lower()
    except:
      continue
    match keystroke:
      case key.ESC:
        player.stop()
  
  # Once the player is in stopped state, release it.
  print("zryte-cli: Stream ended")
  player.release()


def main():
  # Create the top-level command-line argument parser
  parser = argparse.ArgumentParser(prog='zryte-cli',
                                   description="ZryteZene Python CLI")
  subparsers = parser.add_subparsers(dest='subcommand',
                                     required=True)

  # Add subcommands with their arguments
  # The "list" subcommand
  subparsers.add_parser('list')

  # The "stream" subcommand
  subcommand_stream = subparsers.add_parser('stream', description="Play a song via ID")
  subcommand_stream.add_argument('id', type=str, help="specify the song ID to play")

  # The "search" subcommand
  subcommand_search = subparsers.add_parser('search')
  subcommand_search.add_argument('name', type=str, help="specify the song name to look for")

  # The "config" subcommand
  subcommand_config = subparsers.add_parser('config')
  subcommand_config.add_argument('key', type=str, help="specify the config key")
  subcommand_config.add_argument('value', help="specify the new value")
  subcommand_config.add_argument('-s', '--save',
                      action='store_const',
                      const=True,
                      help="overwrite changes to config then exit")

  # Parse the command-line, and use designated functions for which subcommands are used
  args = parser.parse_args()

  match args.subcommand:
    case 'list':
      list()
    case 'stream':
      stream(id=args.id)
      pass
    case 'search':
      list(prefix=args.name)
    case 'config':
      # TODO: config(key, value, ...) function here
      print("zryte-cli: warn: The config subcommand is not yet implemented")
      pass


if __name__ == "__main__":
  main()
