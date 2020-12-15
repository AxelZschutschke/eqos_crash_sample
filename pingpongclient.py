import grpc
import pingpong_pb2
import pingpong_pb2_grpc

channel = grpc.insecure_channel('localhost:51345')
stub = pingpong_pb2_grpc.PingPongStub(channel)

request = pingpong_pb2.Ping()
result = stub.Do( request = request )
print( len( result.data ) )
