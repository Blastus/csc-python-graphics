using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace Boids_Screensaver
{
    static class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            System.Diagnostics.Process python = new System.Diagnostics.Process();
            python.EnableRaisingEvents = false;
            python.StartInfo.FileName = "C:\\Python31\\pythonw.exe";
            python.StartInfo.Arguments = "boids.pyw";
            foreach (string arg in args)
            {
                python.StartInfo.Arguments += " " + arg;
            }
            python.Start();
        }
    }
}