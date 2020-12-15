import grpc 
import pingpong_pb2
import pingpong_pb2_grpc

from concurrent import futures
import numpy as np
from io import BytesIO

class PingPongServer( pingpong_pb2_grpc.PingPongServicer ):
  def __init__( self, messagesize = 10000 ):
    self.multiplier  = 1000
    self.messagesize = messagesize

  def Do( self, request, context ):
    try:
        print( "received:", request )
        context.set_code( grpc.StatusCode.OK )
        data = np.random.rand( self.messagesize, self.multiplier )
        pickle = BytesIO()
        np.save( pickle, data, allow_pickle=False )
        result = pingpong_pb2.Pong( 
                text = "test", 
                data = pickle.getvalue()
                )
        print( "returning:", result.text )
    except Exception as e:
        print( e ) 
    return result


if __name__ == "__main__":
  ping = PingPongServer( messagesize = 20000 )

  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options = [
        ('grpc.max_send_message_length', -1),
        ('grpc.max_receive_message_length', -1)
    ])
  pingpong_pb2_grpc.add_PingPongServicer_to_server(
      ping, server)
  server.add_insecure_port('[::]:51346')
  server.start()
  server.wait_for_termination()

