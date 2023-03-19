from dotenv import load_dotenv
from stream.dj import DJ
from send_email import send_email_when_error


try:
    REFRESH_VIDEO_QUEUE_INTERVAL = 5

    load_dotenv()  # take environment variables from .env.

    if __name__ == "__main__":
        dj = DJ(REFRESH_VIDEO_QUEUE_INTERVAL)
        dj.start_stream()

except:
    print("There is an error!")
    send_email_when_error()
    
        


