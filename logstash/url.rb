require "uri"

def filter(event)
	url = event.get('url')
	if url.nil? or url.empty?
		event.tag('_ip_lookup_failure')
		return [ event ]
	end

	default = '{}'
	begin
      uri = URI.parse(url)

      query = ''
      form = nil
      
      if !uri.query.nil?
        form = URI.decode_www_form(uri.query)
        params = Array.new
      
        for ary in form
          params.push(ary[0])
        end
      
        params = params.sort
      
        nform = Array.new
      
        for ary in params
          nform.push(Array[ary, default])
        end
      
        query = '?' + URI.encode_www_form(nform)
      end 
      
      site = "#{uri.scheme}://#{uri.host}"
      if (uri.scheme == 'http' and uri.port != 80) or (uri.scheme == 'https' and uri.port != 443)
        site = "#{site}:#{uri.port}"
      end

      url_tpl = "#{site}#{uri.path}#{query}"
      if !uri.fragment.nil?
      	url_tpl = "#{url_tpl}##{uri.fragment}"
      end

      event.set('path', uri.path)
      event.set('url_tpl', url_tpl)
      event.set('site', site)
      
      return [ event ]
    rescue => e
      puts("URL parse failed. URL: #{url}, Message: #{e.message}")
      puts(e.backtrace.join("\n"))
      event.tag('_url_lookup_failure')
      return [ event ]
    end
end
