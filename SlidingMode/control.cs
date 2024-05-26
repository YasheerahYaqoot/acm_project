using UnityEngine;
using System.Collections;

using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

public class control : MonoBehaviour
{
    public float X;
    public float Y;
    public float Z;
    public float Roll;
    public float Yaw;
    public float Pitch;

    static Socket listener;
    private CancellationTokenSource source;
    public ManualResetEvent allDone;
    public Renderer objectRenderer;

    public static readonly int PORT = 1755;
    public static readonly int WAITTIME = 1;
    // Start is called before the first frame update
    async void Start()
    {
        source = new CancellationTokenSource();
        allDone = new ManualResetEvent(false);
        X = 0.0f;
        Y = 0.0f;
        Z = 0.0f;
        Pitch = 0.0f;
        Yaw = 0.0f;
        Roll = 0.0f;

        await Task.Run(() => ListenEvents(source.Token));
    }

    void FixedUpdate()
    {
        transform.position = new Vector3(Z, X, Y);
        transform.rotation = Quaternion.Euler(Pitch, Yaw, Roll);


    }
    private void ListenEvents(CancellationToken token)
    {


        IPHostEntry ipHostInfo = Dns.GetHostEntry(Dns.GetHostName());
        IPAddress ipAddress = ipHostInfo.AddressList.FirstOrDefault(ip => ip.AddressFamily == AddressFamily.InterNetwork);
        IPEndPoint localEndPoint = new IPEndPoint(ipAddress, PORT);


        listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);


        try
        {
            listener.Bind(localEndPoint);
            listener.Listen(10);


            while (!token.IsCancellationRequested)
            {
                allDone.Reset();

                print("Waiting for a connection... host :" + ipAddress.MapToIPv4().ToString() + " port : " + PORT);
                listener.BeginAccept(new AsyncCallback(AcceptCallback), listener);

                while (!token.IsCancellationRequested)
                {
                    if (allDone.WaitOne(WAITTIME))
                    {
                        break;
                    }
                }

            }

        }
        catch (Exception e)
        {
            print(e.ToString());
        }
    }

    void AcceptCallback(IAsyncResult ar)
    {
        Socket listener = (Socket)ar.AsyncState;
        Socket handler = listener.EndAccept(ar);

        allDone.Set();

        StateObject state = new StateObject();
        state.workSocket = handler;
        handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReadCallback), state);
    }

    void ReadCallback(IAsyncResult ar)
    {
        StateObject state = (StateObject)ar.AsyncState;
        Socket handler = state.workSocket;

        int read = handler.EndReceive(ar);

        if (read > 0)
        {
            state.colorCode.Append(Encoding.ASCII.GetString(state.buffer, 0, read));
            handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReadCallback), state);
        }
        else
        {
            if (state.colorCode.Length > 1)
            {
                string content = state.colorCode.ToString();
                print($"Read {content.Length} bytes from socket.\n Data : {content}");
                SetColors(content);
            }
            handler.Close();
        }
    }

    //Set color to the MaterialS
    private void SetColors(string data)
    {
        string[] colors = data.Split(',');
        //public float[] forces = new float[4];
        X = float.Parse(colors[0]) / 100.0f;
        Y = float.Parse(colors[1]) / 100.0f;
        Z = float.Parse(colors[2]) / 100.0f;
        Pitch = float.Parse(colors[3]) / 100.0f;
        Yaw = float.Parse(colors[4]) / 100.0f;
        Roll = float.Parse(colors[5]) / 100.0f;


    }

    private void OnDestroy()
    {
        source.Cancel();
    }

    public class StateObject
    {
        public Socket workSocket = null;
        public const int BufferSize = 1024;
        public byte[] buffer = new byte[BufferSize];
        public StringBuilder colorCode = new StringBuilder();
    }

}
