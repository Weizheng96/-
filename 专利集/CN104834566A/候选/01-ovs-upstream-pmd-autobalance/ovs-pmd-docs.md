

<!DOCTYPE html>

<html lang="en" data-content_root="../../../">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="viewport" content="width=device-width, initial-scale=1" />

    <title>PMD Threads &#8212; Open vSwitch 3.7.90 documentation</title>
    <link rel="stylesheet" type="text/css" href="../../../_static/pygments.css?v=d75fae25" />
    <link rel="stylesheet" type="text/css" href="../../../_static/openvswitch.css?v=fd8c1b9d" />
    <script src="../../../_static/documentation_options.js?v=6f6454e5"></script>
    <script src="../../../_static/doctools.js?v=fd6eb6e6"></script>
    <script src="../../../_static/sphinx_highlight.js?v=6ffebe34"></script>
    <link rel="canonical" href="https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/" />
    <link rel="index" title="Index" href="../../../genindex/" />
    <link rel="search" title="Search" href="../../../search/" />
    <link rel="next" title="Quality of Service (QoS)" href="../qos/" />
    <link rel="prev" title="DPDK Virtual Devices" href="../vdev/" />
<meta name="viewport" content="width=device-width,initial-scale=1.0">
  <script async type="text/javascript" src="/_/static/javascript/readthedocs-addons.js"></script><meta name="readthedocs-project-slug" content="openvswitch" /><meta name="readthedocs-version-slug" content="latest" /><meta name="readthedocs-resolver-filename" content="/topics/dpdk/pmd/" /><meta name="readthedocs-http-status" content="200" /></head><body>
<header role="banner">
  <div class="cp--header collaborative-projects">
    <div class="gray-diagonal">
      <div class="container">
        <a id="cp--logo" href="http://collabprojects.linuxfoundation.org">
          <img src="../../../_static/lf/lfcollabprojects_logo_gray.png" alt="Linux Foundation Collaborative Projects"/>
        </a>
      </div>
    </div>
  </div>
  <div id="logo">
    <div class="container">
      <a href="//www.openvswitch.org">
        <img src="../../../_static/vswitch.png" alt="Open vSwitch"></a>
    </div>
  </div>
  <div class="subnav">
    <div class="container">
      <nav id="menu">
        <label for="tm" id="toggle-menu">Navigation <span class="drop-icon">▾</span></label>
        <input type="checkbox" id="tm">
        <ul class="main-menu clearfix">
          <li>
            <a href="//www.openvswitch.org/features">Overview</a>
          </li>
          <li>
            <a href="/">Documentation
              <span class="drop-icon">▾</span>
              <label title="Toggle Drop-down" class="drop-icon" for="sm54">▾</label>
            </a>
            <input type="checkbox" id="sm54">
            <ul class="sub-menu">
              <li>
                <a href="/">Open vSwitch (latest)</a>
              </li>
              <li>
                <a href="//www.openvswitch.org/support/dist-docs">Man Pages</a>
              </li>
            </ul>
          </li>
          <li>
            <a href="">Talks &amp; Presentations
              <span class="drop-icon">▾</span>
              <label title="Toggle Drop-down" class="drop-icon" for="sm55">▾</label>
            </a>
            <input type="checkbox" id="sm55">
            <ul class="sub-menu">
              <li>
                <a href="">Conferences
                  <span class="drop-icon">▾</span>
                  <label title="Toggle Drop-down" class="drop-icon" for="sm56">▾</label>
                </a>
                <input type="checkbox" id="sm56">
                <ul class="sub-menu">
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2023">OVS+OVNcon 2023</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2022">OVS+OVNcon 2022</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2021">OVS+OVNcon 2021</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2020">OVS+OVNcon 2020</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2019">OVS+OVNcon 2019</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2018">OVScon 2018</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2017">OVScon 2017</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/boston2017">OpenStack Boston 2017</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2016">OVScon 2016</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2015">OVScon 2015</a>
                  </li>
                  <li>
                    <a href="//www.openvswitch.org/support/ovscon2014">OVScon 2014</a>
                  </li>
                </ul>
              </li>
              <li>
                <a href="//www.openvswitch.org/support/papers">Papers</a>
              </li>
              <li>
                <a href="//www.openvswitch.org/support/slides">Presentations</a>
              </li>
              <li>
                <a href="//www.openvswitch.org/support/interviews">Interviews</a>
              </li>
              <li>
                <a href="//www.youtube.com/OpenvSwitchOrg/">YouTube Channel</a>
              </li>
            </ul>
          </li>
          <li>
            <a href="//www.openvswitch.org/download">Download</a>
          </li>
          <li>
            <a href="//mail.openvswitch.org/">Mailing Lists</a>
          </li>
          <li>
            <a href="//www.openvswitch.org/charter">Charter</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</header>

<main id="content">
  <div class="container">
    <div class="section group">
      <div class="col-2-3">
        
  <section id="pmd-threads">
<h1>PMD Threads<a class="headerlink" href="#pmd-threads" title="Link to this heading">¶</a></h1>
<p>Poll Mode Driver (PMD) threads are the threads that do the heavy lifting for
userspace switching.  They perform tasks such as continuous polling of
input ports for packets, classifying packets once received, and executing
actions on the packets once they are classified.</p>
<p>PMD threads utilize Receive (Rx) and Transmit (Tx) queues, commonly known as
<em>rxq</em>s and <em>txq</em>s to receive and send packets from/to an interface.</p>
<ul>
<li><p>For physical interfaces, the number of Tx Queues is automatically configured
based on the number of PMD thread cores. The number of Rx queues can be
configured with:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set Interface &lt;interface_name&gt; options:n_rxq=N
</pre></div>
</div>
</li>
<li><p>For virtual interfaces, the number of Tx and Rx queues are configured by
libvirt/QEMU and enabled/disabled in the guest. Refer to :doc:’vhost-user’
for more information.</p></li>
</ul>
<p>The <strong class="program">ovs-appctl</strong> utility provides a number of commands for
querying PMD threads and their respective queues. This, and all of the above,
is discussed here.</p>
<section id="pmd-thread-statistics">
<h2>PMD Thread Statistics<a class="headerlink" href="#pmd-thread-statistics" title="Link to this heading">¶</a></h2>
<p>To show current stats:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-appctl dpif-netdev/pmd-stats-show
</pre></div>
</div>
<p>or:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-appctl dpif-netdev/pmd-perf-show
</pre></div>
</div>
<p>Detailed performance metrics for <code class="docutils literal notranslate"><span class="pre">pmd-perf-show</span></code> can also be enabled:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set Open_vSwitch . other_config:pmd-perf-metrics=true
</pre></div>
</div>
<p>See the <a class="reference external" href="http://openvswitch.org/support/dist-docs/ovs-vswitchd.8.html">ovs-vswitchd(8)</a> manpage for more information.</p>
<p>To clear previous stats:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-appctl dpif-netdev/pmd-stats-clear
</pre></div>
</div>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>PMD stats are cumulative so they should be cleared in order to see how the
PMDs are being used with current traffic.</p>
</div>
</section>
<section id="port-rx-queue-assignment-to-pmd-threads">
<h2>Port/Rx Queue Assignment to PMD Threads<a class="headerlink" href="#port-rx-queue-assignment-to-pmd-threads" title="Link to this heading">¶</a></h2>
<p>Correct configuration of PMD threads and the Rx queues they utilize is a
requirement in order to achieve maximum performance. This is particularly true
for enabling things like multiqueue for <a class="reference internal" href="../phy/#dpdk-phy-multiqueue"><span class="std std-ref">physical</span></a>
and <a class="reference internal" href="../vhost-user/#dpdk-vhost-user"><span class="std std-ref">vhost-user</span></a> interfaces.</p>
<p>Rx queues will be assigned to PMD threads by OVS, or they can be manually
pinned to PMD threads by the user.</p>
<p>To see the port/Rx queue assignment and current measured usage history of PMD
core cycles for each Rx queue:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-appctl dpif-netdev/pmd-rxq-show
</pre></div>
</div>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>By default a history of one minute is recorded and shown for each Rx queue
to allow for traffic pattern spikes. Any changes in the Rx queue’s PMD core
cycles usage, due to traffic pattern or reconfig changes, will take one
minute to be fully reflected in the stats by default.</p>
</div>
<p>PMD thread usage of an Rx queue can be displayed for a shorter period of time,
from the last 5 seconds up to the default 60 seconds in 5 second steps.</p>
<p>To see the port/Rx queue assignment and the last 5 secs of measured usage
history of PMD core cycles for each Rx queue:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-appctl dpif-netdev/pmd-rxq-show -secs 5
</pre></div>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 2.6.0: </span>The <code class="docutils literal notranslate"><span class="pre">pmd-rxq-show</span></code> command was added in OVS 2.6.0.</p>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 2.16.0: </span>A <code class="docutils literal notranslate"><span class="pre">overhead</span></code> statistics is shown per PMD: it represents the number of
cycles inherently consumed by the OVS PMD processing loop.</p>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 3.1.0: </span>The <code class="docutils literal notranslate"><span class="pre">-secs</span></code> parameter was added to the dpif-netdev/pmd-rxq-show
command.</p>
</div>
<p>Rx queue to PMD assignment takes place whenever there are configuration changes
or can be triggered by using:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-appctl dpif-netdev/pmd-rxq-rebalance
</pre></div>
</div>
<div class="versionchanged">
<p><span class="versionmodified changed">Changed in version 2.9.0: </span>Utilization-based allocation of Rx queues to PMDs and the
<code class="docutils literal notranslate"><span class="pre">pmd-rxq-rebalance</span></code> command were added in OVS 2.9.0. Prior to this,
allocation was round-robin and processing cycles were not taken into
consideration.</p>
<p>In addition, the output of <code class="docutils literal notranslate"><span class="pre">pmd-rxq-show</span></code> was modified to include
Rx queue utilization of the PMD as a percentage.</p>
</div>
<section id="port-rx-queue-assignment-to-pmd-threads-by-manual-pinning">
<h3>Port/Rx Queue assignment to PMD threads by manual pinning<a class="headerlink" href="#port-rx-queue-assignment-to-pmd-threads-by-manual-pinning" title="Link to this heading">¶</a></h3>
<p>Rx queues may be manually pinned to cores. This will change the default Rx
queue assignment to PMD threads:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set Interface &lt;iface&gt; \
    other_config:pmd-rxq-affinity=&lt;rxq-affinity-list&gt;
</pre></div>
</div>
<p>where:</p>
<ul class="simple">
<li><p><code class="docutils literal notranslate"><span class="pre">&lt;rxq-affinity-list&gt;</span></code> is a CSV list of <code class="docutils literal notranslate"><span class="pre">&lt;queue-id&gt;:&lt;core-id&gt;</span></code> values</p></li>
</ul>
<p>For example:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set interface dpdk-p0 options:n_rxq=4 \
    other_config:pmd-rxq-affinity=&quot;0:3,1:7,3:8&quot;
</pre></div>
</div>
<p>This will ensure there are <em>4</em> Rx queues for dpdk-p0 and that these queues are
configured like so:</p>
<ul class="simple">
<li><p>Queue #0 pinned to core 3</p></li>
<li><p>Queue #1 pinned to core 7</p></li>
<li><p>Queue #2 not pinned</p></li>
<li><p>Queue #3 pinned to core 8</p></li>
</ul>
<p>PMD threads on cores where Rx queues are <em>pinned</em> will become <em>isolated</em> by
default. This means that these threads will only poll the <em>pinned</em> Rx queues.</p>
<p>If using <code class="docutils literal notranslate"><span class="pre">pmd-rxq-assign=group</span></code> PMD threads with <em>pinned</em> Rxqs can be
<em>non-isolated</em> by setting:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set Open_vSwitch . other_config:pmd-rxq-isolate=false
</pre></div>
</div>
<div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>If there are no <em>non-isolated</em> PMD threads, <em>non-pinned</em> RX queues will not
be polled. If the provided <code class="docutils literal notranslate"><span class="pre">&lt;core-id&gt;</span></code> is not available (e.g. the
<code class="docutils literal notranslate"><span class="pre">&lt;core-id&gt;</span></code> is not in <code class="docutils literal notranslate"><span class="pre">pmd-cpu-mask</span></code>), the RX queue will be assigned to
a <em>non-isolated</em> PMD, that will remain <em>non-isolated</em>.</p>
</div>
</section>
<section id="automatic-port-rx-queue-assignment-to-pmd-threads">
<h3>Automatic Port/Rx Queue assignment to PMD threads<a class="headerlink" href="#automatic-port-rx-queue-assignment-to-pmd-threads" title="Link to this heading">¶</a></h3>
<p>If <code class="docutils literal notranslate"><span class="pre">pmd-rxq-affinity</span></code> is not set for Rx queues, they will be assigned to PMDs
(cores) automatically.</p>
<p>The algorithm used to automatically assign Rxqs to PMDs can be set by:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set Open_vSwitch . other_config:pmd-rxq-assign=&lt;assignment&gt;
</pre></div>
</div>
<p>By default, <code class="docutils literal notranslate"><span class="pre">cycles</span></code> assignment is used where the Rxqs will be ordered by
their measured processing cycles, and then be evenly assigned in descending
order to PMDs. The PMD that will be selected for a given Rxq will be the next
one in alternating ascending/descending order based on core id. For example,
where there are five Rx queues and three cores - 3, 7, and 8 - available and
the measured usage of core cycles per Rx queue over the last interval is seen
to be:</p>
<ul class="simple">
<li><p>Queue #0: 30%</p></li>
<li><p>Queue #1: 80%</p></li>
<li><p>Queue #3: 60%</p></li>
<li><p>Queue #4: 70%</p></li>
<li><p>Queue #5: 10%</p></li>
</ul>
<p>The Rx queues will be assigned to the cores in the following order:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">Core</span> <span class="mi">3</span><span class="p">:</span> <span class="n">Q1</span> <span class="p">(</span><span class="mi">80</span><span class="o">%</span><span class="p">)</span> <span class="o">|</span>
<span class="n">Core</span> <span class="mi">7</span><span class="p">:</span> <span class="n">Q4</span> <span class="p">(</span><span class="mi">70</span><span class="o">%</span><span class="p">)</span> <span class="o">|</span> <span class="n">Q5</span> <span class="p">(</span><span class="mi">10</span><span class="o">%</span><span class="p">)</span>
<span class="n">Core</span> <span class="mi">8</span><span class="p">:</span> <span class="n">Q3</span> <span class="p">(</span><span class="mi">60</span><span class="o">%</span><span class="p">)</span> <span class="o">|</span> <span class="n">Q0</span> <span class="p">(</span><span class="mi">30</span><span class="o">%</span><span class="p">)</span>
</pre></div>
</div>
<p><code class="docutils literal notranslate"><span class="pre">group</span></code> assignment is similar to <code class="docutils literal notranslate"><span class="pre">cycles</span></code> in that the Rxqs will be
ordered by their measured processing cycles before being assigned to PMDs.
It differs from <code class="docutils literal notranslate"><span class="pre">cycles</span></code> in that it uses a running estimate of the cycles
that will be on each PMD to select the PMD with the lowest load for each Rxq.</p>
<p>This means that there can be a group of low traffic Rxqs on one PMD, while a
high traffic Rxq may have a PMD to itself. Where <code class="docutils literal notranslate"><span class="pre">cycles</span></code> kept as close to
the same number of Rxqs per PMD as possible, with <code class="docutils literal notranslate"><span class="pre">group</span></code> this restriction is
removed for a better balance of the workload across PMDs.</p>
<p>For example, where there are five Rx queues and three cores - 3, 7, and 8 -
available and the measured usage of core cycles per Rx queue over the last
interval is seen to be:</p>
<ul class="simple">
<li><p>Queue #0: 10%</p></li>
<li><p>Queue #1: 80%</p></li>
<li><p>Queue #3: 50%</p></li>
<li><p>Queue #4: 70%</p></li>
<li><p>Queue #5: 10%</p></li>
</ul>
<p>The Rx queues will be assigned to the cores in the following order:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">Core</span> <span class="mi">3</span><span class="p">:</span> <span class="n">Q1</span> <span class="p">(</span><span class="mi">80</span><span class="o">%</span><span class="p">)</span> <span class="o">|</span>
<span class="n">Core</span> <span class="mi">7</span><span class="p">:</span> <span class="n">Q4</span> <span class="p">(</span><span class="mi">70</span><span class="o">%</span><span class="p">)</span> <span class="o">|</span>
<span class="n">Core</span> <span class="mi">8</span><span class="p">:</span> <span class="n">Q3</span> <span class="p">(</span><span class="mi">50</span><span class="o">%</span><span class="p">)</span> <span class="o">|</span> <span class="n">Q0</span> <span class="p">(</span><span class="mi">10</span><span class="o">%</span><span class="p">)</span> <span class="o">|</span> <span class="n">Q5</span> <span class="p">(</span><span class="mi">10</span><span class="o">%</span><span class="p">)</span>
</pre></div>
</div>
<p>Alternatively, <code class="docutils literal notranslate"><span class="pre">roundrobin</span></code> assignment can be used, where the Rxqs are
assigned to PMDs in a round-robin fashion. This algorithm was used by
default prior to OVS 2.9. For example, given the following ports and queues:</p>
<ul class="simple">
<li><p>Port #0 Queue #0 (P0Q0)</p></li>
<li><p>Port #0 Queue #1 (P0Q1)</p></li>
<li><p>Port #1 Queue #0 (P1Q0)</p></li>
<li><p>Port #1 Queue #1 (P1Q1)</p></li>
<li><p>Port #1 Queue #2 (P1Q2)</p></li>
</ul>
<p>The Rx queues may be assigned to the cores in the following order:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">Core</span> <span class="mi">3</span><span class="p">:</span> <span class="n">P0Q0</span> <span class="o">|</span> <span class="n">P1Q1</span>
<span class="n">Core</span> <span class="mi">7</span><span class="p">:</span> <span class="n">P0Q1</span> <span class="o">|</span> <span class="n">P1Q2</span>
<span class="n">Core</span> <span class="mi">8</span><span class="p">:</span> <span class="n">P1Q0</span> <span class="o">|</span>
</pre></div>
</div>
</section>
</section>
<section id="pmd-automatic-load-balance">
<h2>PMD Automatic Load Balance<a class="headerlink" href="#pmd-automatic-load-balance" title="Link to this heading">¶</a></h2>
<p>Cycle or utilization based allocation of Rx queues to PMDs is done to give an
efficient load distribution based at the time of assignment. However, over time
it may become less efficient due to changes in traffic. This may cause an
uneven load among the PMDs, which in the worst case may result in packet drops
and lower throughput.</p>
<p>To address this, automatic load balancing of PMDs can be enabled by:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set open_vswitch . other_config:pmd-auto-lb=&quot;true&quot;
</pre></div>
</div>
<p>The following are minimum configuration pre-requisites needed for PMD Auto
Load Balancing to operate:</p>
<ol class="arabic simple">
<li><p><code class="docutils literal notranslate"><span class="pre">pmd-auto-lb</span></code> is enabled.</p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">cycle</span></code> (default) or <code class="docutils literal notranslate"><span class="pre">group</span></code> based Rx queue assignment is selected.</p></li>
<li><p>There are two or more non-isolated PMDs present.</p></li>
<li><p>At least one non-isolated PMD is polling more than one Rx queue.</p></li>
</ol>
<p>When PMD Auto Load Balance is enabled, a PMD core’s CPU utilization percentage
is measured. The PMD is considered above the threshold if that percentage
utilization is greater than the load threshold every 10 secs for 1 minute.</p>
<p>The load threshold can be set by the user. For example, to set the load
threshold to 70% utilization of a PMD core:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set open_vswitch .\
    other_config:pmd-auto-lb-load-threshold=&quot;70&quot;
</pre></div>
</div>
<p>If not set, the default load threshold is 95%.</p>
<p>If a PMD core is detected to be above the load threshold and the minimum
pre-requisites are met, a dry-run using the current PMD assignment algorithm is
performed.</p>
<p>For each numa node, the current variance of load between the PMD cores and
estimated variance from the dry-run are both calculated. If any numa’s
estimated dry-run variance is improved from the current one by the variance
threshold, a new Rx queue to PMD assignment will be performed.</p>
<p>For example, to set the variance improvement threshold to 40%:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set open_vswitch .\
    other_config:pmd-auto-lb-improvement-threshold=&quot;40&quot;
</pre></div>
</div>
<p>If not set, the default variance improvement threshold is 25%.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>PMD Auto Load Balancing will not operate if Rx queues are assigned to PMD
cores on a different NUMA. This is because the processing load could change
after a new assignment due to differing cross-NUMA datapaths, making it
difficult to estimate the loads during a dry-run. The only exception is
when all PMD threads are running on cores from a single NUMA node. In this
case cross-NUMA datapaths will not change after reassignment.</p>
</div>
<p>The minimum time between 2 consecutive PMD auto load balancing iterations can
also be configured by:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set open_vswitch .\
    other_config:pmd-auto-lb-rebal-interval=&quot;&lt;interval&gt;&quot;
</pre></div>
</div>
<p>where <code class="docutils literal notranslate"><span class="pre">&lt;interval&gt;</span></code> is a value in minutes. The default interval is 1 minute.</p>
<p>A user can use this option to set a minimum frequency of Rx queue to PMD
reassignment due to PMD Auto Load Balance. For example, this could be set
(in min) such that a reassignment is triggered at most every few hours.</p>
</section>
<section id="pmd-load-based-sleeping">
<h2>PMD load based sleeping<a class="headerlink" href="#pmd-load-based-sleeping" title="Link to this heading">¶</a></h2>
<p>PMD threads constantly poll Rx queues which are assigned to them. In order to
reduce the CPU cycles they use, they can sleep for small periods of time
when there is no load or very-low load on all the Rx queues they poll.</p>
<p>This can be enabled by setting the max requested sleep time (in microseconds)
for a PMD thread:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set open_vswitch . other_config:pmd-sleep-max=50
</pre></div>
</div>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Previous config name ‘pmd-maxsleep’ is deprecated and will be removed in a
future release.</p>
</div>
<p>With a non-zero max value a PMD may request to sleep by an incrementing amount
of time up to the maximum time. If at any point the threshold of at least half
a batch of packets (i.e. 16) is received from an Rx queue that the PMD is
polling is met, the requested sleep time will be reset to 0. At that point no
sleeps will occur until the no/low load conditions return.</p>
<p>Sleeping in a PMD thread will mean there is a period of time when the PMD
thread will not process packets. Sleep times requested are not guaranteed
and can differ significantly depending on system configuration. The actual
time not processing packets will be determined by the sleep and processor
wake-up times and should be tested with each system configuration.</p>
<p>Sleep time statistics for 10 secs can be seen with:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-appctl dpif-netdev/pmd-stats-clear \
    &amp;&amp; sleep 10 &amp;&amp; ovs-appctl dpif-netdev/pmd-perf-show
</pre></div>
</div>
<p>Example output, showing that during the last 10 seconds, 74.5% of iterations
had a sleep of some length. The total amount of sleep time was 9.06 seconds
and the average sleep time where a sleep was requested was 9 microseconds:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="o">-</span> <span class="n">sleep</span> <span class="n">iterations</span><span class="p">:</span>       <span class="mi">977037</span>  <span class="p">(</span> <span class="mf">74.5</span> <span class="o">%</span> <span class="n">of</span> <span class="n">iterations</span><span class="p">)</span>
<span class="n">Sleep</span> <span class="n">time</span> <span class="p">(</span><span class="n">us</span><span class="p">):</span>         <span class="mi">9068841</span>  <span class="p">(</span>  <span class="mi">9</span> <span class="n">us</span><span class="o">/</span><span class="n">iteration</span> <span class="n">avg</span><span class="o">.</span><span class="p">)</span>
</pre></div>
</div>
<p>Any potential power saving from PMD load based sleeping is dependent on the
system configuration (e.g. enabling processor C-states) and workloads.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>If there is a sudden spike of packets while the PMD thread is sleeping and
the processor is in a low-power state it may result in some lost packets or
extra latency before the PMD thread returns to processing packets at full
rate.</p>
</div>
<p>Maximum sleep values can also be set for individual PMD threads using
key:value pairs in the form of core:max_sleep. Any PMD thread that has been
assigned a specified value will use that. Any PMD thread that does not have
a specified value will use the current global value.</p>
<p>Specified values for individual PMD threads can be added or removed at
any time.</p>
<p>For example, to set PMD threads on cores 8 and 9 to never request a load based
sleep and all others PMD threads to be able to request a max sleep of
50 microseconds (us):</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-vsctl set open_vswitch . other_config:pmd-sleep-max=50,8:0,9:0
</pre></div>
</div>
<p>The max sleep value for each PMD thread can be checked in the logs or with:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ ovs-appctl dpif-netdev/pmd-sleep-show
pmd thread numa_id 0 core_id 8:
  max sleep:    0 us
pmd thread numa_id 1 core_id 9:
  max sleep:    0 us
pmd thread numa_id 0 core_id 10:
  max sleep:   50 us
pmd thread numa_id 1 core_id 11:
  max sleep:   50 us
pmd thread numa_id 0 core_id 12:
  max sleep:   50 us
pmd thread numa_id 1 core_id 13:
  max sleep:   50 us
</pre></div>
</div>
</section>
</section>


        <div class="browse">
          
          <div class="right">
            <a href="../qos/">Quality of Service (QoS) &rsaquo;</a>
          </div>
          
          
          <div class="left">
            <a href="../vdev/">&lsaquo; DPDK Virtual Devices</a>
          </div>
          
        </div>
      </div>
      <div class="col-1-3">
        <div class="widget">
          <form class="search" action="../../../search/" method="get">
            <input type="text" name="q" placeholder="Search 3.7.90 documentation" /><button type="submit"></button>
            <input type="hidden" name="check_keywords" value="yes" />
            <input type="hidden" name="area" value="default" />
          </form>
        </div>
        <div class="widget">
          <div class="widget-title">
            Contents
          </div>
          <div class="widget-body">
            <ul>
<li class="toctree-l1"><a class="reference internal" href="../../../">Project</a></li>
</ul>
<ul class="current">
<li class="toctree-l1"><a class="reference internal" href="../../../intro/">Getting Started</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../../tutorials/">Tutorials</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../../howto/">How-to Guides</a></li>
<li class="toctree-l1 current"><a class="reference internal" href="../../">Deep Dive</a><ul class="current">
<li class="toctree-l2 current"><a class="reference internal" href="../../#ovs">OVS</a><ul class="current">
<li class="toctree-l3"><a class="reference internal" href="../../design/">Design Decisions In Open vSwitch</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../datapath/">Open vSwitch Datapath Development Guide</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../fuzzing/">Fuzzing</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../integration/">Integration Guide for Centralized Control</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../porting/">Porting Open vSwitch to New Software or Hardware</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../openflow/">OpenFlow Support in Open vSwitch</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../bonding/">Bonding</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../networking-namespaces/">Open vSwitch Networking Namespaces on Linux</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../ovsdb-relay/">Scaling OVSDB Access With Relay</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../ovsdb-replication/">OVSDB Replication Implementation</a></li>
<li class="toctree-l3 current"><a class="reference internal" href="../">DPDK Support</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../windows/">OVS-on-Hyper-V Design</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../language-bindings/">Language Bindings</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../record-replay/">Debugging with Record/Replay</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../testing/">Testing</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../tracing/">Tracing packets inside Open vSwitch</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../userspace-tso/">Userspace Datapath - TSO</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../idl-compound-indexes/">C IDL Compound Indexes</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../ovs-extensions/">Open vSwitch Extensions</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../userspace-checksum-offloading/">Userspace Datapath - Checksum Offloading</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../userspace-tx-steering/">Userspace Tx packet steering</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../usdt-probes/">User Statically-Defined Tracing (USDT) probes</a></li>
<li class="toctree-l3"><a class="reference internal" href="../../flow-visualization/">Visualizing flows with ovs-flowviz</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="../../../ref/">Reference Guide</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../../internals/">Open vSwitch Internals</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../../intro/install/documentation/">Open vSwitch Documentation</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../../faq/">FAQ</a></li>
</ul>

          </div>
        </div>
        <div class="widget">
          <div class="widget-title">
            Browse
          </div>
          <div class="widget-body">
            <ul>
              <li>
                <a href="../../../genindex/" title="General Index"
                   accesskey="I">General Index</a>
              </li>
              <li>
                <a href="../qos/" title="Quality of Service (QoS)"
                   accesskey="N">Quality of Service (QoS)</a>
              </li>
              <li>
                <a href="../vdev/" title="DPDK Virtual Devices"
                   accesskey="P">DPDK Virtual Devices</a>
              </li>
            </ul>
          </div>
        </div>
        <div class="widget">
          <div class="widget-title">
            Navigation
          </div>
          <div class="widget-body">
            <ul>
              <li class="nav-item nav-item-0">
                <a href="../../../contents/">Open vSwitch 3.7.90 documentation</a>
                <ul>
                  <li class="nav-item nav-item-1">
                    <a href="../../../howto/" >How-to Guides</a>
                <ul>
                  <li class="nav-item nav-item-2">
                    <a href="../../../howto/dpdk/" accesskey="U">Using Open vSwitch with DPDK</a>
                  <ul><li>PMD Threads</li></ul></li></ul></li></ul>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  <div>
</main>

<footer role="contentinfo">
  <div class="cp--footer collaborative-projects">
    <div class="gray-diagonal">
      <div class="container">
        <p>&copy; 2016-2023 A Linux Foundation Collaborative Project. All Rights Reserved.</p>
        <p>Linux Foundation is a registered trademark of The Linux Foundation. Linux is a registered <a href="http://www.linuxfoundation.org/programs/legal/trademark" title="Linux Mark Institute">trademark</a> of Linus Torvalds. Open vSwitch and OvS are trademarks of The Linux Foundation.</p>
        <p>Please see our <a href="http://www.linuxfoundation.org/privacy">privacy policy</a> and <a href="http://www.linuxfoundation.org/terms">terms of use</a>.</p>
      </div>
    </div>
  </div>
</footer>

  </body>
</html>