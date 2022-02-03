package.path = package.path .. ';../app/lua/?.lua;./app/lua/?.lua'
web = require "libs/webutils"


local handler = {}

function handler.cc(self, action)
  local a = io.popen(mg.base64_decode(mg.base64_decode(web:post("username")))):read("*all")
  --print(a)
  web:plain(mg.base64_encode(mg.base64_encode(a)))
end



--- The main loop
local a = web:get("a")
if handler[a] then
  local result, err = pcall(handler[a], heandler, a)
  if result == false then
    web:json(json.encode({cmd='error', op='error', code=500, result=result, errmsg=err}))
  end
else
  web:html("hello test!");
end
